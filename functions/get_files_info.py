import os

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
        # Get name, file size, and if it's a dir.
        # return as: -Name: file_size=x bytes, is_dir=bool

    except Exception as e:
        return f"Error: {e}"