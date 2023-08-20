"""
A module to run Automatabot, a code analyzer and fixer, which uses static code
analysis and the Automata Agent to find and fix issues in code.
"""

from automatabot.analyzers import Analyzer
from automatabot.utils.analyze_directory import analyze_directory

from automata.cli.scripts.run_agent import main as run_agent_main

from difflib import unified_diff
from unidiff import PatchSet

from typing import List, Optional
import diff_match_patch as dmp_module
import re

import logging
import logging.config

from automata.core.utils import get_logging_config, get_root_fpath

from automata.code_parsers.py import PyReader
from automata.code_writers.py.py_code_writer import PyCodeWriter
from automata.singletons.py_module_loader import py_module_loader


logger = logging.getLogger(__name__)
logging.config.dictConfig(get_logging_config())

class Automatabot:
    """A class to run Automatabot on a codebase."""
    def __init__(self) -> None:
        self.diff = None
        self.file_path: Optional[str] = None
        self.issues = None
        self.root_path = get_root_fpath()

    def generate_issues(self, directory_path: str, ignored_directories: Optional[List[str]]) -> None:
        """Generate a dict of issues from the codebase."""
        logger.info("Generating issues...")

        analyzer = Analyzer()
        analyzer.set_analysis_types("snake_case")

        issues = analyze_directory(
            analyzer,
            directory_path,
            ignored_directories,
        )
        self.issues = issues
    
    def run_automatabot(self) -> str:
        """Run Automatabot on a codebase."""
        self.generate_issues("/Users/nolantremelling/automata/automata", ["automata-embedding-data", "docs", "scip-python"])

        if self.issues:  # Check if there are any issues
            issue = self.issues[0]  # Get the first issue
            instruction = f"{issue['issue']}: {issue['prompt']}"
            self.file_path = issue["file"]
            print(f"{instruction}\n")

        return run_agent_main(
            instructions=instruction,
            model="gpt-4",
            toolkits="agent-search,py-reader,py-interpreter",
            log_level="DEBUG",
            max_iterations=20
        )

    def extract_code_from_agent(self, response: str) -> Optional[str]:
        """Extract code from the agent's output."""
        pattern = r'```python\n(.*?)```'
        match = re.search(pattern, response, re.DOTALL)
        return match[1] if match else None

    def generate_diff(self, fixed_code: str) -> None:
        """Generate a diff between the original code and the fixed code."""
        if self.file_path:
            with open(self.file_path, 'r') as f:
                original_code = f.read()

        # Generate the unified diff using difflib
        diff_lines = list(unified_diff(
            original_code.splitlines(),
            fixed_code.splitlines(),
            #fromfile="first_version.py",
            #tofile="modified_version.py",
            lineterm=''))

        # Convert the unified diff lines to a single string
        unified_diff_str = '\n'.join(diff_lines)

        # Save the unified diff to a file
        with open("automata/bot/generated_diff.txt", 'w') as diff_file:
            diff_file.write(unified_diff_str)



if __name__ == "__main__":
    
    bot = Automatabot()
    agent_response = bot.run_automatabot()
    parsed_agent_response = bot.extract_code_from_agent(agent_response)
    print("fixed_file: ", parsed_agent_response)
    if parsed_agent_response:
        bot.generate_diff(parsed_agent_response)
    py_reader = PyReader()
    py_writer = PyCodeWriter(py_reader)
    py_module_loader.initialize()
    py_writer._process_diff_file("/Users/nolantremelling/automata/automata/bot/generated_diff.txt", "automata.tests.unit.cli.test_cli_scripts_run_doc_embedding")
    py_writer.apply_diff("/Users/nolantremelling/automata/automata/bot/generated_diff.py", "/Users/nolantremelling/automata/automata/tests/unit/cli/test_cli_scripts_run_code_embedding.py")