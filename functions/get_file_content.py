import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        current_dir = os.path.abspath(working_directory)
        joined_file_path = os.path.join(working_directory, file_path)
        absolute_file_path = os.path.normpath(os.path.abspath(joined_file_path))
        
        valid_file_path = os.path.commonpath([absolute_file_path, current_dir]) == current_dir

        if not valid_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(absolute_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(absolute_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {e}"