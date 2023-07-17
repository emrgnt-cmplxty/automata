from automata.singletons.dependency_factory import dependency_factory
from automata.singletons.py_module_loader import py_module_loader


def initialize_automata():
    py_module_loader.reset()
    dependency_factory.reset()
    py_module_loader.initialize()
