import ast

from automata.code_parsers.py import PyReader
from automata.code_writers.py.py_code_writer import PyCodeWriter
from automata.singletons.py_module_loader import py_module_loader


def hello_world():
    print("Hello from PyCodeWriter!")
