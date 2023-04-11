import ast
import os


class ObjectInfo:
    def __init__(self, name, docstring, code):
        self.name = name
        self.docstring = docstring
        self.code = code

    def get_raw_code(self):
        return self.code

    def get_doc_string(self):
        return self.docstring


class FileObject:
    def __init__(self, filepath, docstring, standalone_functions, classes):
        self.filepath = filepath
        self.docstring = docstring
        self.standalone_functions = standalone_functions
        self.classes = classes

    def get_standalone_functions(self):
        return self.standalone_functions

    def get_classes(self):
        return self.classes

    def get_docstring(self):
        return self.docstring


class CodeParser:
    def __init__(self):
        self.file_dict = {}

    def populate_file_dict(self, root_dir):
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        node = ast.parse(f.read())

                    docstring = ast.get_docstring(node)
                    standalone_functions = []
                    classes = []
                    for n in node.body:
                        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            func_name = n.name
                            func_docstring = ast.get_docstring(n)
                            func_code = "".join(ast.unparse(n))
                            function = ObjectInfo(func_name, func_docstring, func_code)
                            standalone_functions.append(function)
                        elif isinstance(n, ast.ClassDef):
                            class_name = n.name
                            class_docstring = ast.get_docstring(n)
                            class_code = "".join(ast.unparse(n))
                            class_obj = ObjectInfo(class_name, class_docstring, class_code)
                            classes.append(class_obj)

                    self.file_dict[file] = FileObject(
                        file_path, docstring, standalone_functions, classes
                    )

    def lookup_code(self, object_name):
        for file_obj in self.file_dict.values():
            for obj in file_obj.get_standalone_functions() + file_obj.get_classes():
                if obj.name == object_name:
                    return obj.get_raw_code()
        return None

    def lookup_docstring(self, object_name):
        for file_obj in self.file_dict.values():
            for obj in file_obj.get_standalone_functions() + file_obj.get_classes():
                if obj.name == object_name:
                    return obj.get_doc_string()
        return None

    def get_standalone_functions(self, file_name):
        if file_name in self.file_dict:
            return [func.name for func in self.file_dict[file_name].get_standalone_functions()]
        return None

    def get_classes(self, file_name):
        if file_name in self.file_dict:
            return [cls.name for cls in self.file_dict[file_name].get_classes()]
        return None

    def lookup_file_docstring(self, file_name):
        if file_name in self.file_dict:
            return self.file_dict[file_name].get_docstring()
        return None


if __name__ == "__main__":
    print("Performing code lookup")
    code_parser = CodeParser()
    code_parser.populate_file_dict("../")
    print("Done loading the Code Parser")
    print("Login Github:\n%s" % (code_parser.lookup_code("login_github")))
    print("Lookup Docstring:\n%s" % (code_parser.lookup_docstring("login_github")))
    print("Get StandAlone Functions:\n%s" % (code_parser.get_standalone_functions("utils.py")))
    print("Get Classes:\n%s" % (code_parser.get_classes("utils.py")))
    print("Lookup File DocString:\n%s" % (code_parser.lookup_file_docstring("utils.py")))
