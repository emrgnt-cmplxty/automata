import logging
import os

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    GenerationConfig,
    LlamaForCausalLM,
    LlamaTokenizer,
    StoppingCriteria,
    StoppingCriteriaList,
)

logger = logging.getLogger(__name__)


class LocalLLamaModel:
    """A class to provide zero-shot completions from a local Llama model."""

    # TODO - Make these upstream configurations
    MAX_OUTPUT_LENGTH = 2048
    TOP_K = 40
    TOP_P = 0.9
    NUM_BEAMS = 1

    def __init__(
        self,
        model: str,
        temperature: float,
        hf_access_token: str,
        max_output_length=None,
    ) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Selecting device = {self.device}")

        self.hf_access_token = hf_access_token
        self.max_output_length = (
            max_output_length or LocalLLamaModel.MAX_OUTPUT_LENGTH
        )
        self.tokenizer = LlamaTokenizer.from_pretrained(
            model,
            torch_dtype=torch.float16,
            device_map="auto",
            use_auth_token=self.hf_access_token,
        )

        self.model = LlamaForCausalLM.from_pretrained(
            model,
            torch_dtype=torch.float16,
            device_map="auto",
            use_auth_token=self.hf_access_token,
        )
        self.temperature = temperature

    def get_completion(self, prompt: str, *args, **kwargs) -> str:
        """Generate the completion from the local Llama model."""
        # TODO - Move all configurations upstream

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        generation_config = GenerationConfig(
            temperature=self.temperature,
            top_p=LocalLLamaModel.TOP_P,
            top_k=LocalLLamaModel.TOP_K,
            num_beams=LocalLLamaModel.NUM_BEAMS,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.pad_token_id,
            do_sample=True,
        )

        output = self.model.generate(
            inputs["input_ids"],
            generation_config=generation_config,
            do_sample=True,
            max_new_tokens=self.max_output_length,
        )

        output = output[0].to(self.device)
        return self.tokenizer.decode(output)


HUMANEVAL_EOS = [
    "\nclass",
    "\ndef",
    "\n#",
    "\n@",
    "\nprint",
    "\nif",
    "\n\n\n\n\n",
]
NON_CODE_EOS = [
    "<|endoftext|>",
    "\n```",
    "\n</s>",
    "<|endofmask|>",
    "</s>",
    "<EOT>",
]
EOS = HUMANEVAL_EOS + NON_CODE_EOS


# Adopted from https://github.com/huggingface/transformers/pull/14897
class EndOfFunctionCriteria(StoppingCriteria):
    def __init__(self, start_length, eos, tokenizer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_length = start_length
        self.eos = eos
        self.tokenizer = tokenizer
        self.end_length = {}

    def __call__(self, input_ids, scores, **kwargs):
        """Returns true if all generated sequences contain any of the end-of-function strings."""
        decoded_generations = self.tokenizer.batch_decode(
            input_ids[:, self.start_length :]
        )
        done = []
        for index, decoded_generation in enumerate(decoded_generations):
            finished = any(
                [stop_string in decoded_generation for stop_string in self.eos]
            )
            if (
                finished and index not in self.end_length
            ):  # ensures first time we see it
                for stop_string in self.eos:
                    if stop_string in decoded_generation:
                        self.end_length[index] = len(
                            input_ids[
                                index,  # get length of actual generation
                                self.start_length : -len(
                                    self.tokenizer.encode(
                                        stop_string,
                                        add_special_tokens=False,
                                        return_tensors="pt",
                                    )[0]
                                ),
                            ]
                        )
            done.append(finished)
        return all(done)


CODE_LLAMA_ROOT = os.environ.get("CODE_LLAMA_ROOT", "/JawTitan/codellama/")


# S1: Install package from https://github.com/facebookresearch/codellama
# S2: Install model to ${CODE_LLAMA_ROOT} (This can be any actual path)
# S3: CODE_LLAMA_ROOT=?? torchrun --nproc_per_node 1 codegen/generate.py --model code-llama-7b --bs 1 --temperature 0 --n_samples 1 --resume --greedy
class CodeLlama:
    def __init__(
        self,
        model: str,
        temperature: float,
    ) -> None:
        assert CODE_LLAMA_ROOT is not None
        from llama import (  # See https://github.com/facebookresearch/codellama
            Llama,
        )

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Selecting device = {self.device}")
        self.generator = Llama.build(
            ckpt_dir=os.path.join(CODE_LLAMA_ROOT, model),
            tokenizer_path=os.path.join(
                CODE_LLAMA_ROOT, model, "tokenizer.model"
            ),
            max_seq_len=512,
            max_batch_size=1,
        )
        self.temperature = temperature

    @staticmethod
    def sanitize(gen_str: str):
        tmp = ""
        for line in str.splitlines(gen_str):
            lspace = len(line) - len(line.lstrip())
            if lspace == 3:
                tmp += " "
            tmp += line + "\n"
        new_code = tmp
        return new_code

    def get_completion(self, prompt: str, *args, **kwargs) -> str:
        gen_strs = self.generator.text_completion(
            [prompt],
            max_gen_len=512,
            temperature=self.temperature,
            top_p=0.95,
        )
        gen_str = [gen_str["generation"] for gen_str in gen_strs][0]

        min_index = 10000
        for eos in EOS:
            if eos in gen_str:
                # could be multiple eos in outputs, better pick minimum one
                min_index = min(min_index, gen_str.index(eos))

        return self.sanitize(prompt + gen_str[:min_index])


# HUGGING_FACE VARIANTS OF CODE LLAMA, doesn't seem to work as well as the local version
class LocalCodeLLamaModel:
    def __init__(
        self,
        model: str,
        temperature: float,
        hf_access_token: str,
        max_output_length=None,
    ) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Selecting device = {self.device}")

        self.max_output_length = (
            max_output_length or LocalLLamaModel.MAX_OUTPUT_LENGTH
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model)

        self.model = AutoModelForCausalLM.from_pretrained(
            model,
            torch_dtype=torch.float16,
            device_map="auto",
        )
        self.temperature = temperature

    @staticmethod
    def sanitize(gen_str: str):
        tmp = ""
        for line in str.splitlines(gen_str):
            lspace = len(line) - len(line.lstrip())
            if lspace == 3:
                tmp += " "
            tmp += line + "\n"
        new_code = tmp
        return new_code

    def get_completion(self, prompt: str, *args, **kwargs) -> str:
        inputs = self.tokenizer.encode(prompt.strip(), return_tensors="pt").to(
            self.device
        )
        scores = StoppingCriteriaList(
            [
                EndOfFunctionCriteria(
                    start_length=len(inputs[0]),
                    eos=EOS,
                    tokenizer=self.tokenizer,
                )
            ]
        )
        raw_outputs = self.model.generate(
            inputs,
            max_new_tokens=512,
            stopping_criteria=scores,
            do_sample=True,
            top_p=LocalLLamaModel.TOP_P,
            top_k=LocalLLamaModel.TOP_K,
            temperature=self.temperature,
            output_scores=True,
            return_dict_in_generate=True,
            num_return_sequences=LocalLLamaModel.NUM_BEAMS,
            pad_token_id=self.tokenizer.eos_token_id,
        )  # remove warning

        gen_seqs = raw_outputs.sequences[:, len(inputs[0]) :]
        gen_str = self.tokenizer.batch_decode(gen_seqs)[0]

        min_index = 10000
        for eos in EOS:
            if eos in gen_str:
                # could be multiple eos in outputs, better pick minimum one
                min_index = min(min_index, gen_str.index(eos))

        return self.sanitize(prompt + gen_str[:min_index]).strip()
