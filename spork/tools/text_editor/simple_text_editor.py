import enum
import os


class EditorState(enum.Enum):
    BEGIN = 1
    OPEN = 2
    EDIT = 3
    END = 4


class SimpleTextEditor:
    def __init__(self):
        self.file_path = None
        self.lines = []
        self.state = EditorState.BEGIN
        self.log = []

    def open_file(self, file_path):
        self.file_path = file_path
        if not os.path.exists(file_path):
            raise ValueError("File does not exist.")

        with open(file_path, "r") as file:
            self.lines = file.readlines()
            self.log.append(f"Opened file {file_path}")

    def create_file(self, file_path):
        self.file_path = file_path
        if os.path.exists(file_path):
            raise ValueError("File already exists.")

        self.lines = []
        self.log.append(f"Created file {file_path}")

    def insert_line(self, line_number, full_line_text):
        if line_number < 0 or line_number > len(self.lines):
            raise IndexError(
                f"Error: insert`{line_number}`{full_line_text}; {line_number} is out of range [0, {len(self.lines)}]"
            )

        self.lines.insert(line_number, full_line_text + "\n")

    def delete_line(self, line_number):
        if line_number < 0 or line_number >= len(self.lines):
            raise IndexError(f"Error: delete`{line_number}; line doesn't exist")

        del self.lines[line_number]

    def replace_line(self, line_number, new_line_text):
        if line_number < 0 or line_number >= len(self.lines):
            raise IndexError(f"Error: replace`{line_number}`{new_line_text}; line doesn't exist")
        self.lines[line_number] = new_line_text + "\n"

    def save_file(self):
        with open(self.file_path, "w") as file:
            file.writelines(self.lines)

    def execute_commands(self, commands: str):
        commands_list = commands.strip().split(";\n")
        for i, command in enumerate(commands_list):
            cmd_parts = command.strip().split("`")
            if cmd_parts[0] == "create":
                if self.state != EditorState.BEGIN:
                    raise ValueError(f"Command {i}: Invalid state transition: create")
                self.create_file(cmd_parts[1])
                self.state = EditorState.EDIT
            if cmd_parts[0] == "begin":
                if self.state != EditorState.BEGIN:
                    raise ValueError(f"Command {i}: Invalid state transition: begin")
                self.state = EditorState.OPEN
            elif cmd_parts[0] == "open":
                if self.state != EditorState.OPEN:
                    raise ValueError(f"Command {i}: Invalid state transition: open")
                self.open_file(cmd_parts[1])
                self.state = EditorState.EDIT
            elif cmd_parts[0] == "insert":
                if self.state != EditorState.EDIT:
                    raise ValueError(f"Command {i}: Invalid state transition: insert")
                self.insert_line(int(cmd_parts[1]), cmd_parts[2])
            elif cmd_parts[0] == "delete":
                if self.state != EditorState.EDIT:
                    raise ValueError(f"Command {i}: Invalid state transition: delete")
                self.delete_line(int(cmd_parts[1]))
            elif cmd_parts[0] == "replace":
                if self.state != EditorState.EDIT:
                    raise ValueError(f"Command {i}: Invalid state transition: replace")
                self.replace_line(int(cmd_parts[1]), cmd_parts[2])
            elif cmd_parts[0] == "end;":
                if self.state != EditorState.EDIT:
                    raise ValueError(f"Command {i}: Invalid state transition: end")
                self.save_file()
                break
            else:
                raise ValueError(f"Invalid command {i}: {cmd_parts[0]}")
        return f"Edits completed successfully! File {self.file_path} saved with {len(self.lines)} lines."

    def reset(self):
        self.file_path = None
        self.lines = []
        self.state = EditorState.BEGIN


# editor = SimpleTextEditor()
# commands = """
# begin;
# open`test_file.txt;
# insert`0`This is a new line;
# insert`1`This is a new line also;
# replace`0`This is a replaced line;
# end;
#
# """
# editor.execute_commands(commands)
