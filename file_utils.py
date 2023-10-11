import os

def file_exists(folder_path, file_name):
    # Combine folder path and file name to create the full file path
    file_path = os.path.join(folder_path, file_name)
    
    # Check if the file exists at the given file path
    return os.path.isfile(file_path)

import json

def load_json(file_path):
    """
    Load JSON content from a file.
    
    Parameters:
    file_path (str): The path to the JSON file.

    Returns:
    dict: A dictionary containing the JSON content.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_json(file_path, data):
    """
    Write JSON content to a file.
    
    Parameters:
    file_path (str): The path to the file where JSON content will be written.
    data (dict): A dictionary containing the JSON content.
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
