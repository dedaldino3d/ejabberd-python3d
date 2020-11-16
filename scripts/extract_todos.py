import os
import time

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN_PACKAGE_DIRECTORY = os.path.join('ejabberd_python3d', ROOT_DIR)
WRITE_FILE_NAME = "TODOS.md"


def create_file():
    f = open(WRITE_FILE_NAME, 'w')
    # f = open(os.path.join(WRITE_FILE_NAME, ROOT_DIR), 'w')
    return f


def report_callee(filename, filewrite):
    print("==> Writing todos in :{} from :{}".format(filewrite, filename))


skip_dirs = ['build', 'dist', '__pycache__', '.git', '.idea', 'ejabberd_python3d.egg-info']


def extract_todos(dir, debug=False):
    if os.path.isdir(dir):
        file = create_file()
        for root, dirs, files in os.walk((dir if os.path.isabs(dir) else os.path.abspath(dir))):
            for d in skip_dirs:
                if d in dirs:
                    dirs.remove(d)
            for f in files:
                try:
                    with open(os.path.join(f, root), 'r') as fr:
                        line = fr.readline()
                        if line.startswith("# TODO") or line.find("TODO"):
                            file.writelines(line)
                            if debug:
                                report_callee(f, file.name)
                        time.sleep(1)
                except PermissionError:
                    print("PermissionError. file: {:<25} dir: {}".format(f, root))
            time.sleep(0.5)
    else:
        raise ValueError("Enter a valid dir name")


if __name__ == '__main__':
    extract_todos(MAIN_PACKAGE_DIRECTORY, debug=True)
