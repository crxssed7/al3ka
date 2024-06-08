import os
import json

def open_file(file):
    with open(f"../json/{file}", "r", encoding="utf8") as file:
        contents = file.read()
        jayson = json.loads(contents)
        return jayson["id"], jayson["volumes"]

def write_file(file, mediaId, volumes):
    with open(f"../json/{file}", "w", encoding="utf8") as file:
        content = json.dumps({
            "id": mediaId,
            "volumes": volumes
        }, indent=4)
        file.write(content)

def list_files_in_directory(directory_path):
    try:
        # Get a list of all entries in the directory
        with os.scandir(directory_path) as entries:
            # Filter out directories, keep only file names
            files = [entry.name for entry in entries if entry.is_file()]
        files.sort()
        return files
    except FileNotFoundError:
        print(f"The directory {directory_path} does not exist.")
        return []
    except PermissionError:
        print(f"Permission denied to access the directory {directory_path}.")
        return []
