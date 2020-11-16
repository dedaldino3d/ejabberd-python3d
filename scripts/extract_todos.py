import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN_PACKAGE_DIRECTORY = os.path.join(ROOT_DIR, 'ejabberd_python3d')
WRITE_FILE_NAME = os.path.join(ROOT_DIR, "TODOS.md")
DEBUG = False


def create_file():
    f = open(WRITE_FILE_NAME, 'w')
    return f


def report_callee(filename, filewrite, line):
    print("==> Writing Todos in {} from: {}\nTODO ==> {}".format(filewrite, filename, line))


skip_dirs = ['build', 'dist', '__pycache__', '.git', '.idea', 'ejabberd_python3d.egg-info']

file2write = create_file()


def extract_todos(dir):
    if os.path.isdir(dir):
        for root, dirs, files in os.walk((dir if os.path.isabs(dir) else os.path.abspath(dir))):
            for d in skip_dirs:
                if d in dirs:
                    dirs.remove(d)
            _extract_todos(files, root)
    else:
        raise ValueError("Enter a valid dir name")


def _extract_todos(files, root):
    if len(files) == 0:
        return
    try:
        file = files.pop()
        _extract_todos2(file, root)
        return _extract_todos(files, root)
    except (IndexError, PermissionError,):
        pass


def _extract_todos2(file, root, ):
    with open(os.path.join(root, file), 'r') as fr:
        for line in fr:
            if "# TODO" in line:
                file2write.writelines(line)
                if DEBUG:
                    report_callee(file, file2write.name, line)


if __name__ == '__main__':
    extract_todos(MAIN_PACKAGE_DIRECTORY)
