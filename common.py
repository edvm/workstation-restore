import subprocess
import inspect
import shlex


def tell_user(msg, stcode=None):
    """Print a message to stdout."""

    def error(msg):
        print(f"\033[1;31;40m[ERROR]\x1b[0;37m {msg}")

    def success(msg):
        print(f"\033[1;32;40m[OK]\x1b[0;37m {msg}")

    def info(msg):
        print(f"\033[1;37;40m>>>\x1b[0;37m {msg}")

    if stcode == 0:
        return success("Previous command was excecuted with success.")
    if stcode != None and stcode != 0:
        return error("Previous command failed.")

    return info(msg)


def execute(cmd):
    """Execute given cmd with subprocess. Return its returncode."""
    process = subprocess.run(shlex.split(cmd))
    returncode = process.returncode
    tell_user('', stcode=returncode)
    return returncode


def module_fns_list(module):
    """Return functions found in given module."""
    for member in inspect.getmembers(module):
        if inspect.isfunction(member[1]):
            yield member
