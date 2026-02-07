import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to file location.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Location of the file.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write to the file."
            ),
        },
    required=["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content):
    try:
        current_dir = os.path.abspath(working_directory)
        joined_file_path = os.path.join(current_dir, file_path)
        absolute_file_path = os.path.normpath(os.path.abspath(joined_file_path))
        
        valid_file_path = os.path.commonpath([absolute_file_path, current_dir]) == current_dir

        if not valid_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(absolute_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'        

        parent_dir = os.path.dirname(absolute_file_path)
        os.makedirs(parent_dir, exist_ok=True)

        with open(absolute_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"