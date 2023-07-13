import pytest
from automata.code_parsers import DirectoryManager

@pytest.fixture
def dir_manager_and_path(tmp_path):
    """
    Creates a test directory structure under the given path.
    """
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir2").mkdir()
    (tmp_path / "dir1" / "file1").write_text("content")
    (tmp_path / "dir1" / "file2").write_text("content")
    (tmp_path / "dir2" / "file1").write_text("content")
    path_str = str(tmp_path)
    return DirectoryManager(path_str), path_str


def test_load_directory_structure(dir_manager_and_path):
    dir_manager, path_str = dir_manager_and_path
    assert dir_manager.root.name == path_str
    assert len(dir_manager.root.children) == 2  # 2 directories: dir1, dir2



def test_get_node_for_path(dir_manager_and_path):
    dir_manager, _ = dir_manager_and_path
    dir1_node = dir_manager._get_node_for_path(dir_manager.root, "dir1")
    assert dir1_node is not None
    assert dir1_node.name == "dir1"
    assert len(dir1_node.children) == 2  # 2 files in dir1: file1, file2


def test_get_files_in_dir(dir_manager_and_path):
    dir_manager, _ = dir_manager_and_path
    files_in_dir1 = dir_manager.get_files_in_dir("dir1")
    assert len(files_in_dir1) == 2  # 2 files in dir1: file1, file2
    assert set(files_in_dir1) == {"file1", "file2"}


def test_get_subdirectories(dir_manager_and_path):
    dir_manager, _ = dir_manager_and_path
    subdirectories = dir_manager.get_subdirectories(".")
    assert len(subdirectories) == 2  # 2 subdirectories in root: dir1, dir2
    assert set(subdirectories) == {"dir1", "dir2"}
