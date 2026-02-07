import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        current_dir = os.path.abspath(working_directory)
        joined_file_path = os.path.join(current_dir, file_path)
        absolute_file_path = os.path.normpath(os.path.abspath(joined_file_path))
        
        valid_file_path = os.path.commonpath([absolute_file_path, current_dir]) == current_dir

        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not absolute_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", absolute_file_path]
        if args is not None:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=current_dir,
            capture_output=True,
            text=True,
            timeout=30,
            )
        
        output = ""
        
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"

        if not result.stdout and not result.stderr:
            output += f"No output produced"
        else:
            if result.stdout:
                output += f"STDOUT:{result.stdout}"
            if result.stderr:
                output += f"STDERR:{result.stderr}"

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"