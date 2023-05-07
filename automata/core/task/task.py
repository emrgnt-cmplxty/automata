import logging
import os
import shutil
import sqlite3
import uuid
import zipfile
from enum import Enum
from io import BytesIO
from typing import Optional

import requests
from github import Github
from retrying import retry

from automata.config import DEFAULT_REMOTE_URL, GITHUB_API_KEY
from automata.core.agent.automata_agent_helpers import (
    create_builder_from_args,
    create_instruction_payload,
)
from automata.core.utils import root_path

JOB_DIR_NAME = "jobs"


class GitHubManager:
    def __init__(self, access_token: str, remote_url: str, remote_branch: str = "main"):
        self.client = Github(access_token)
        self.remote_url = remote_url
        self.remote_branch = remote_branch

    def clone_repository(self, local_path: str):
        # Fetch the archive link from GitHub using the client
        remote_name = self.remote_url.replace("https://github.com/", "")
        repo = self.client.get_repo(remote_name)

        # Fetch the repository archive
        archive_url = repo.get_archive_link("zipball", ref=self.remote_branch)
        response = requests.get(archive_url)

        # Extract the contents of the ZIP file
        with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
            zip_file.extractall()

        # Move the contents of the extracted folder to a new folder with the repository name
        for folder in os.listdir():
            if folder.startswith(f"{repo.owner.login}-{repo.name}-"):
                shutil.move(folder, local_path)
                break

    def sync_task(self, task):
        # Sync task to GitHub (e.g., create/update issue, create/update file)
        pass


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class AutomataTask:
    def __init__(self, github_manager: GitHubManager, *args, **kwargs):
        self.github_manager = github_manager
        self.task_id = uuid.uuid4()  # Unique task ID

        self.priority = kwargs.get("priority", 0)
        self.max_retries = kwargs.get("max_retries", 3)
        self.status = TaskStatus(kwargs.get("status", "pending"))

        builder = create_builder_from_args(*args, **kwargs)
        self.agent = builder.build()
        self.result = None
        self.error: Optional[str] = None
        self.retry_count = 0

    def create_task_env(self):
        # Generate a unique directory name for the task
        task_dir_name = f"task_{self.task_id}"
        self.job_dir = os.path.join(root_path(), JOB_DIR_NAME)
        self.task_dir = os.path.join(self.job_dir, task_dir_name)

        # Create the jobs directory if it does not exist
        if not os.path.exists(self.job_dir):
            os.makedirs(self.job_dir)

        self.github_manager.clone_repository(self.task_dir)

    def wait_exponential(self, retry_state):
        return (2**retry_state.attempt_number) * 1000  # Exponential backoff in milliseconds

    @retry(
        retry_on_exception=lambda e: isinstance(e, Exception),
        wait_func=wait_exponential,
        stop_max_attempt_number=lambda self: self.max_retries,
    )
    def execute(self) -> Optional[str]:
        self.create_task_env()
        self.status = TaskStatus.RUNNING
        try:
            # self.result = self.agent.run()
            self.status = TaskStatus.SUCCESS
        except Exception as e:
            logging.exception(f"AutomataTask failed: {e}")
            self.error = str(e)
            self.status = TaskStatus.FAILED
            self.retry_count += 1
            raise

        return self.result


class TaskDatabase:
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                priority INTEGER,
                status TEXT,
                result TEXT,
                error TEXT,
                retry_count INTEGER,
                access_token TEXT,
                remote_url TEXT,
                remote_branch TEXT
            )
        """
        )
        self.conn.commit()

    def insert_task(self, task: AutomataTask) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO tasks (task_id, priority, status, result, error, retry_count, access_token, remote_url, remote_branch)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                task.task_id,
                task.priority,
                task.status.value,
                task.result,
                task.error,
                task.retry_count,
                task.github_manager.remote_url,
                task.github_manager.remote_branch,
            ),
        )
        self.conn.commit()

    def update_task(self, task: AutomataTask) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE tasks SET
                priority = ?,
                status = ?,
                result = ?,
                error = ?,
                retry_count = ?,
                access_token = ?,
                remote_url = ?,
                remote_branch = ?
            WHERE task_id = ?
        """,
            (
                task.priority,
                task.status.value,
                task.result,
                task.error,
                task.retry_count,
                task.github_manager.remote_url,
                task.github_manager.remote_branch,
                task.task_id,
            ),
        )
        self.conn.commit()

    def get_task(self, task_id: str) -> Optional[AutomataTask]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
        row = cursor.fetchone()

        if row:
            github_manager = GitHubManager(
                access_token=GITHUB_API_KEY, remote_url=row[7], remote_branch=row[8]
            )
            task = AutomataTask(github_manager=github_manager)
            task.task_id = row[0]
            task.priority = row[1]
            task.status = TaskStatus(row[2])
            task.result = row[3]
            task.error = row[4]
            task.retry_count = row[5]
            return task
        else:
            return None


class TaskRegistry:
    def __init__(self, db: TaskDatabase):
        self.db = db

    def add_task(self, task: AutomataTask) -> None:
        self.db.insert_task(task)

    def get_task(self, task_id) -> Optional[AutomataTask]:
        return self.db.get_task(task_id)


if __name__ == "__main__":
    print("Running a task...")
    from automata.configs.automata_agent_configs import AutomataAgentConfig
    from automata.configs.config_enums import AgentConfigVersion

    instruction_payload = create_instruction_payload(overview="Overview", agents_message="Message")
    github_manager = GitHubManager(access_token=GITHUB_API_KEY, remote_url=DEFAULT_REMOTE_URL)

    task = AutomataTask(
        agent_config=AutomataAgentConfig.load(AgentConfigVersion.AUTOMATA_INDEXER_DEV),
        llm_toolkits="",
        model="gpt-4",
        instruction_payload=instruction_payload,
        stream=True,
        github_manager=github_manager,
    )
    task.create_task_env()
