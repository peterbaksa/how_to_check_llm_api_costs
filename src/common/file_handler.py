import os

def get_cwd(project_name):
    if not project_name in os.getcwd():
        raise ValueError(f"Project name '{project_name}' not found in current working directory.")
    return os.getcwd().split(project_name)[0]+project_name
