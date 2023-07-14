import logging
import os
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class Node:
    """Abstract base class for a node in the file tree"""

    def __init__(self, name: str, parent: Optional["Node"] = None) -> None:
        """
        Args:
            name (str): Name of the node
            parent (Node): Parent node of this node
        """
        self.name = name
        self.parent = parent


class File(Node):
    """Represents a file in the tree"""

    def __init__(self, name: str, parent: Optional["Node"] = None) -> None:
        """
        Args:
            name (str): Name of the file
            parent (Node): Parent node of this file
        """
        super().__init__(name, parent)


class Directory(Node):
    """Represents a directory. Has children which can be directories or files"""

    def __init__(self, name: str, parent: Optional["Node"] = None) -> None:
        """
        Args:
            name (str): Name of the directory
            parent (Node): Parent node of this directory
        """
        super().__init__(name, parent)
        self.children: Dict[str, Node] = {}

    def add_child(self, child: "Node") -> None:
        """
        Adds a child node to this directory

        Args:
            child (Node): Child node to add
        """
        self.children[child.name] = child

    def get_file_names(self) -> List[str]:
        """
        Get a list of file names in the directory

        Args:
            directory (Directory): Directory to get file names from

        Returns:
            List[str]: List of file names in the directory
        """
        return [
            name
            for name, child in self.children.items()
            if isinstance(child, File)
        ]

    def get_subdirectories(self) -> List[str]:
        """
        Get a list of subdirectory names in the directory

        Args:
            directory (Directory): Directory to get subdirectory names from

        Returns:
            List[str]: List of subdirectory names in the directory
        """
        return [
            name
            for name, child in self.children.items()
            if isinstance(child, Directory)
        ]

    def is_root_dir(self) -> bool:
        """
        Check if this directory is the root directory

        Returns:
            bool: True if this directory is the root directory, False otherwise
        """
        return self.parent is None

    def is_leaf_dir(self) -> bool:
        """
        Check if this directory is a leaf directory (has no subdirectories)

        Returns:
            bool: True if this directory is a leaf directory, False otherwise
        """
        subdirectories = [
            child
            for child in self.children.values()
            if isinstance(child, Directory) and "__pycache__" not in child.name
        ]
        return not subdirectories


class DirectoryManager:
    """Handles operations related to directory structure."""

    def __init__(self, base_path: str) -> None:
        """
        Args:
            base_path (str): Base path of the directory structure
        """
        self.root = self._load_directory_structure(base_path)

    def _load_directory_structure(self, root_dir: str) -> "Directory":
        """Load directory structure into Directory and File objects."""
        root = Directory(root_dir)
        self.root = root  # Set root before walking through directory

        # Map of directory paths to their corresponding nodes
        dir_path_to_node = {root_dir: root}

        for parent_dir, dirs, files in os.walk(root_dir):
            # Find the parent directory node
            parent_node = dir_path_to_node[parent_dir]

            # Add all directories
            for dir in dirs:
                dir_node = Directory(dir, parent_node)
                parent_node.add_child(dir_node)
                dir_path_to_node[os.path.join(parent_dir, dir)] = dir_node

            # Add all files
            for file in files:
                parent_node.add_child(File(file, parent_node))

        return root

    def get_files_in_dir(self, path: str) -> List[str]:
        """
        Get a list of files in the given directory

        Args:
            path (str): Path of the directory

        Returns:
            List[str]: List of files in the directory
        """
        dir_node = self._get_node_for_path(self.root, path)
        if dir_node and isinstance(dir_node, Directory):
            return dir_node.get_file_names()
        else:
            return []

    def get_subdirectories(self, path: str) -> List[str]:
        """
        Get a list of subdirectories in the given directory

        Args:
            path (str): Path of the directory

        Returns:
            List[str]: List of subdirectories in the directory
        """
        dir_node = self._get_node_for_path(self.root, path)
        if dir_node and isinstance(dir_node, Directory):
            return dir_node.get_subdirectories()
        else:
            return []

    def ensure_directory_exists(self, directory_path: str) -> None:
        """
        Creates the directory if it does not exist already

        Args:
            directory_path (str): Path of the directory to create
        """
        if not os.path.exists(directory_path):
            logger.info(f"Creating directory_path = {directory_path}")
            os.makedirs(directory_path)
            self.root = self._load_directory_structure(directory_path)

    def _get_node_for_path(
        self, root: "Directory", path: str
    ) -> Optional["Node"]:
        """
        Find the node for a given path

        Args:
            root (Directory): Root node of the tree
            path (str): Path to find the node for

        Returns:
            Optional[Node]: Node for the given path, None if not found
        """

        if path == ".":
            return root

        path_parts = path.split(os.sep)
        # Initial node is root
        node: Directory = root

        # Iterate through path parts
        for part in path_parts:
            if part not in node.children:
                # If part not found in children, return None
                return None

            new_node = node.children[part]
            if not isinstance(new_node, Directory):
                # If part is a file, return None
                return None
            node = new_node
        return node
