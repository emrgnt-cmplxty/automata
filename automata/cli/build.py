import os
import pathlib
import shutil
import subprocess

script_dir = pathlib.Path(__file__).parent.absolute()
automata_root = script_dir.parent.parent
repo_store_path = os.path.join(automata_root.parent, "repo_store")
embedding_data_path = os.path.relpath(
    os.path.join(automata_root, "automata-embedding-data"), automata_root
)
factory_path = os.path.relpath(
    os.path.join(automata_root, "automata_embedding_factory"), automata_root
)
project_name = "automata"
repo_store_project_path = os.path.join(repo_store_path, project_name)
scip_python_path = os.path.join(automata_root, "scip-python")
pyright_scip_index = os.path.join(
    scip_python_path, "packages", "pyright-scip", "index"
)
project_in_factory = os.path.join(factory_path, project_name)


def git(*args):
    return subprocess.check_call(["git"] + list(args))


def install_indexing():
    try:
        os.chdir(scip_python_path)
        subprocess.run(["npm", "install"], check=True)

        os.chdir(os.path.join(scip_python_path, "packages/pyright-scip"))
        subprocess.run(["npm", "run", "build"], check=True)
    finally:
        os.chdir(automata_root)


def generate_remote_indices():
    if os.path.exists(repo_store_project_path):
        shutil.rmtree(repo_store_project_path)

    git(
        "clone",
        "git@github.com:emrgnt-cmplxty/Automata.git",
        repo_store_project_path,
    )

    project_indices = os.path.join(
        embedding_data_path, "indices", f"{project_name}.scip"
    )
    if os.path.exists(project_indices):
        os.remove(project_indices)

    if os.path.exists(factory_path):
        shutil.rmtree(factory_path)
    os.makedirs(factory_path)
    shutil.move(repo_store_project_path, factory_path)

    node_command = f"node {pyright_scip_index} index --project-name {project_name} --output {embedding_data_path}/indices/{project_name}.scip  --target-only {project_name}"
    subprocess.run(node_command, shell=True)

    shutil.move(project_in_factory, repo_store_project_path)


def generate_local_indices():
    project_indices = os.path.join(
        embedding_data_path, "indices", f"{project_name}.scip"
    )
    if os.path.exists(project_indices):
        os.remove(project_indices)

    if os.path.exists(factory_path):
        shutil.rmtree(factory_path)
    os.makedirs(factory_path)

    def ignore_dirs(src, names):
        ignored_dirs = ["automata_embedding_factory", "scip-python"]
        return [name for name in names if name in ignored_dirs]

    shutil.copytree(automata_root, project_in_factory, ignore=ignore_dirs)

    node_command = "node scip-python/packages/pyright-scip/index index --project-name automata --output automata-embedding-data/indices/automata.scip --target-only automata"
    subprocess.run(node_command, shell=True)
