from dotenv import load_dotenv


def get_key(dotenv_path, key_to_get):
    """Get an existing key from a .env file."""
    with open(dotenv_path, "r") as file:
        lines = file.readlines()

    for line in lines:
        key, _, value = line.partition("=")
        if key == key_to_get:
            return value.rstrip()


def replace_key(dotenv_path, key_to_set, value_to_set):
    """Replace an existing key in a .env file."""
    with open(dotenv_path, "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        key, _, _ = line.partition("=")
        if key == key_to_set:
            lines[i] = f"{key_to_set}={value_to_set}\n"

    with open(dotenv_path, "w") as file:
        file.writelines(lines)


def load_env_vars(DOTENV_PATH, DEFAULT_KEYS):
    load_dotenv()

    for key, default_value in DEFAULT_KEYS.items():
        current_value = get_key(DOTENV_PATH, key)
        if current_value is None:
            raise ValueError(f"Key {key} not found in the .env file")
        elif not current_value or current_value == default_value:
            new_value = input(
                f"{key} is not configured. Please enter your key: "
            )
            replace_key(DOTENV_PATH, key, new_value)


def show_key_value(DOTENV_PATH, key):
    value = get_key(DOTENV_PATH, key)
    print(f"The value of {key} is: {value}")


def update_key_value(DOTENV_PATH, key):
    new_value = input(f"Enter new value for {key}: ")
    replace_key(DOTENV_PATH, key, new_value)
    print(f"The value of {key} has been updated.")


def delete_key_value(DOTENV_PATH, key):
    user_confirmation = input(
        f"Are you sure you want to delete the value of {key}? [y/n]: "
    )
    if user_confirmation.lower() == "y":
        replace_key(DOTENV_PATH, key, "")
        print(f"The value of {key} has been deleted.")
    else:
        print(f"Operation cancelled. The value of {key} has not been deleted.")
