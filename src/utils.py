import yaml

def load_config(config_file_path: str) -> dict:
    """
    Loads a YAML configuration file and returns its contents as a dictionary.

    Args:
        config_file_path (str): The file path to the YAML configuration file.

    Returns:
        dict: The contents of the YAML file as a dictionary.
    """
    try:
        with open(config_file_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file {config_file_path} not found.")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file: {e}")
