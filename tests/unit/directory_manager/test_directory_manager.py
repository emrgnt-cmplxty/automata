from automata.code_parsers import DirectoryManager


def create_test_dir_structure(tmp_path):
    """
    Creates a test directory structure under the given path.
    """
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir2").mkdir()
    (tmp_path / "dir1" / "file1").write_text("content")
    (tmp_path / "dir1" / "file2").write_text("content")
    (tmp_path / "dir2" / "file1").write_text("content")
    return tmp_path


def test_load_directory_structure(tmp_path):
    test_dir = create_test_dir_structure(tmp_path)
    dir_manager = DirectoryManager(str(test_dir))
    assert dir_manager.root.name == str(test_dir)
    assert len(dir_manager.root.children) == 2  # 2 directories: dir1, dir2


def test_get_node_for_path(tmp_path):
    test_dir = create_test_dir_structure(tmp_path)
    dir_manager = DirectoryManager(str(test_dir))
    dir1_node = dir_manager._get_node_for_path(dir_manager.root, "dir1")
    assert dir1_node is not None
    assert dir1_node.name == "dir1"
    assert len(dir1_node.children) == 2  # 2 files in dir1: file1, file2


def test_get_files_in_dir(tmp_path):
    test_dir = create_test_dir_structure(tmp_path)
    dir_manager = DirectoryManager(str(test_dir))
    files_in_dir1 = dir_manager.get_files_in_dir("dir1")
    assert len(files_in_dir1) == 2  # 2 files in dir1: file1, file2
    assert set(files_in_dir1) == {"file1", "file2"}


def test_get_subdirectories(tmp_path):
    test_dir = create_test_dir_structure(tmp_path)
    dir_manager = DirectoryManager(str(test_dir))
    subdirectories = dir_manager.get_subdirectories(".")
    assert len(subdirectories) == 2  # 2 subdirectories in root: dir1, dir2
    assert set(subdirectories) == {"dir1", "dir2"}
