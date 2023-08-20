import ast

from automata.code_parsers.py import PyReader
from automata.code_writers.py.py_code_writer import PyCodeWriter
from automata.singletons.py_module_loader import py_module_loader

if __name__ == "__main__":
    py_reader = PyReader()
    py_writer = PyCodeWriter(py_reader)
    py_module_loader.initialize()
    module_dotpath = "automata.eval.agent.test_script"
    script_content = py_reader.get_source_code(module_dotpath)
    original_module_ast = ast.parse(script_content)
    module_ast = ast.parse(script_content)
    for node in module_ast.body:
        if isinstance(node, ast.FunctionDef) and node.name == "hello_world":
            for sub_node in node.body:
                if isinstance(sub_node, ast.Expr) and isinstance(
                    sub_node.value, ast.Call
                ):
                    call_node = sub_node.value
                    if (
                        isinstance(call_node.func, ast.Name)
                        and call_node.func.id == "print"
                    ):
                        call_node.args = [
                            ast.Str(s="Hello from PyCodeWriter!")
                        ]
    updated_script = ast.unparse(module_ast)
    print(updated_script)
    py_writer.upsert_to_module(
        py_module_loader.fetch_ast_module(module_dotpath), module_ast
    )
    py_writer.write_module_to_disk(module_dotpath)
