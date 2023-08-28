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
