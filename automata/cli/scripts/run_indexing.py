import os
import subprocess


def main():
    script_dir = os.path.join(os.path.dirname(__file__), "../../../scripts")
    install_script = os.path.join(script_dir, "install_indexing.sh")
    regenerate_script = os.path.join(script_dir, "regenerate_index.sh")

    subprocess.check_call(["sh", install_script])
    subprocess.check_call(["sh", regenerate_script])
