import sys
import os

def get_project_dir(project_name="my_tushare"):
    for path in sys.path:
        if project_name in path:
            path = path.split(project_name)
            if len(path) == 2:
                return os.path.join(path[0], project_name)

project_dir = get_project_dir()
code_data_dir = "code_data"
