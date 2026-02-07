import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        current_dir = os.path.abspath(working_directory)

        target_dir = os.path.normpath(
            os.path.join(current_dir, directory)
        )

        valid_target_dir = os.path.commonpath([current_dir, target_dir]) == current_dir

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        entries = os.listdir(target_dir)

        lines = []
        for name in entries:
            full_path = os.path.join(target_dir, name)
            size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            line = f'- {name}: file_size={size} bytes, is_dir={is_dir}'
            lines.append(line)
        result = '\n'.join(lines)
        return result

    except Exception as e:
        return f"Error: {e}"