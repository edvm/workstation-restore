import subprocess
import shlex
import os


HOME = os.getenv("HOME")
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))


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


def execute(cmd, env=None):
    """Execute given cmd with subprocess. Return its returncode."""
    process = subprocess.run(shlex.split(cmd), env=env)
    returncode = process.returncode
    tell_user('', stcode=returncode)
    return returncode

