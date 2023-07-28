import os

fallback_data_root_path = "automata-embedding-data"
data_root_path = os.environ.get("DATA_ROOT_PATH", fallback_data_root_path)
