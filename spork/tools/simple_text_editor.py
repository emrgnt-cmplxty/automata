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

    def open_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        self.file_path = file_path
        with open(file_path, "r") as file:
            self.lines = file.readlines()

    def insert_line(self, line_number, full_line_text):
        if line_number < 0 or line_number > len(self.lines):
            raise IndexError("Invalid line number")

        self.lines.insert(line_number, full_line_text + "\n")

    def delete_line(self, line_number):
        if line_number < 0 or line_number >= len(self.lines):
            raise IndexError("Invalid line number")

        del self.lines[line_number]

    def replace_line(self, line_number, new_line_text):
        if line_number < 0 or line_number >= len(self.lines):
            raise IndexError("Invalid line number")
        self.lines[line_number] = new_line_text + "\n"

    def save_file(self):
        with open(self.file_path, "w") as file:
            file.writelines(self.lines)

    def execute_commands(self, commands: str):
        commands_list = commands.strip().split(";\n")
        for command in commands_list:
            cmd_parts = command.strip().split("`")

            if cmd_parts[0] == "begin":
                if self.state != EditorState.BEGIN:
                    raise ValueError("Invalid state transition: begin")
                self.state = EditorState.OPEN
            elif cmd_parts[0] == "open":
                if self.state != EditorState.OPEN:
                    raise ValueError("Invalid state transition: open")
                self.open_file(cmd_parts[1])
                self.state = EditorState.EDIT
            elif cmd_parts[0] == "insert":
                if self.state != EditorState.EDIT:
                    raise ValueError("Invalid state transition: insert")
                self.insert_line(int(cmd_parts[1]), cmd_parts[2])
            elif cmd_parts[0] == "delete":
                if self.state != EditorState.EDIT:
                    raise ValueError("Invalid state transition: delete")
                self.delete_line(int(cmd_parts[1]))
            elif cmd_parts[0] == "replace":
                if self.state != EditorState.EDIT:
                    raise ValueError("Invalid state transition: replace")
                self.replace_line(int(cmd_parts[1]), cmd_parts[2])
            elif cmd_parts[0] == "end;":
                if self.state != EditorState.EDIT:
                    raise ValueError("Invalid state transition: end")
                self.save_file()
                self.state = EditorState.BEGIN
                break
            else:
                raise ValueError(f"Invalid command: {cmd_parts[0]}")
        return "Edits completed successfully!"


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
