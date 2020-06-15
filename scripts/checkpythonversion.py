import sys

def check_right_version():
    if sys.version_info[0] > 2 and sys.version_info[1] > 5:
        print(f'Python version is ok: {sys.version}'})
    else:
        raise PythonVersionException('This tool requires Python 3.6 or higher')
