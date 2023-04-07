from bokeh.models import Tool
from langchain.agents import tool


class GitToolBuilder:
    def __init__(self, github_repo, pygit_repo, issue):
        self.github_repo = github_repo
        self.pygit_repo = pygit_repo
        self.issue = issue

    def build_tools(self):
        tools = [
            Tool(
                name="git-branch",
                func=lambda input_str: self.create_new_branch(input_str),
                description="Creates and checks out a new branch in the specified repository. The only input is the branch name. For exmpale: 'my-branch'",
                return_direct=False,
            ),
            Tool(
                name="git-commit",
                func=lambda input_str: self.commit_to_git(input_str),
                description="Takes a string of comma-separated file names and commits them to git. For example 'file1.py,file2.py'",
                return_direct=False,
            ),
            Tool(
                name="git-create-pull-request",
                func=lambda input_str: self.create_pull_request(input_str),
                description="Creates a pull request in the specified repository.",
                return_direct=False,
            ),
        ]
        return tools

    def create_new_branch(self, branch_name: str) -> str:
        """
        Creates and checks out a new branch in the specified repository. The only input is the branch name. For exmpale: "my-branch"
        """
        # Create branch
        self.pygit_repo.git.branch(branch_name)
        # Checkout branch
        self.pygit_repo.git.checkout(branch_name)

        return f"Created and checked out branch {branch_name} in {self.github_repo.name} repository."

    def commit_to_git(self, file_names: str) -> str:
        """
        Takes a string of comma-separated file names and commits them to git. For example "file1.py,file2.py"
        """
        file_names = file_names.split(",")
        for file_name in file_names:
            self.pygit_repo.git.add(file_name)

        self.pygit_repo.git.commit(m="Committing changes")
        self.pygit_repo.git.push(
            "--set-upstream", "origin", self.pygit_repo.git.branch("--show-current")
        )
        return f"Committed {file_names} to {self.github_repo.name} repository."

    def create_pull_request(self, body) -> str:
        """
        Creates a pull request in the specified repository.
        """
        # get current branch name
        current_branch = self.pygit_repo.git.branch("--show-current")
        title = "Fix for issue #" + str(self.issue.number)
        self.github_repo.create_pull(
            head=current_branch, base=self.github_repo.default_branch, issue=self.issue
        )
        return (
            f"Created pull request for  {title} in {self.github_repo.name} repository."
        )
