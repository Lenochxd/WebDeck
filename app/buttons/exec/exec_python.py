def execute_python_file(file_path):
    with open(file_path, "r") as file:
        file_content = file.read()
    exec(file_content)