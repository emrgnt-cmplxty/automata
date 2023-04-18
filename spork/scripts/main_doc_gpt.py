import argparse

from spork.tools.documentation_tools.documentation_gpt import DocumentationGPT

parser = argparse.ArgumentParser(description="Configure documentation chat system")
parser.add_argument(
    "--url",
    "-u",
    type=str,
    help="URL of the documentation",
    default="https://python.langchain.com/en/latest/",
)
parser.add_argument(
    "--model",
    "-m",
    type=str,
    help="LLM to use",
    default="gpt-4",
    choices=["gpt-3.5-turbo", "gpt-4"],
)
parser.add_argument(
    "--temperature", "-t", type=float, help="temperature of the model", default=0.7
)
parser.add_argument("--verbose", "-v", action="store_true", help="increase output verbosity")

if __name__ == "__main__":
    args = parser.parse_args()

    # load the documentation

    doc_gpt = DocumentationGPT(
        url=args.url,
        model=args.model,
        temperature=args.temperature,
        verbose=args.verbose,
    )
    doc_gpt.run()
