import os


def convert_fpath_to_module_dotpath(root_abs_path, module_path):
    module_rel_path = (os.path.relpath(module_path, root_abs_path).replace(os.path.sep, "."))[:-3]
    return module_rel_path
