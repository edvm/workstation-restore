import subprocess
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


def excecute(cmd):
    """Excecute given cmd with subprocess. Return its returncode."""
    process = subprocess.run(shlex.split(cmd))
    returncode = process.returncode
    _tell('', stcode=returncode)
    return returncode