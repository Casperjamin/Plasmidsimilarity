import sys

def check_right_version():
    if sys.version_info[0] > 2 and sys.version_info[1] > 5:
        sys.stderr.write(f'Python version is ok: {sys.version}\n')
    else:
        raise PythonVersionException(f'This tool requires Python 3.6 or higher.\t You are using {sys.version}')
