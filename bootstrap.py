#!/usr/bin/env python

import subprocess
import pathlib
import shutil
import shlex
import sys
import os


HOME = os.getenv('HOME')

KITTY_TERMINAL_DEFAULT_THEME = "3024_Night.conf"  # default kitty term name


VSCODE_GPG_KEY_CMD = '''
sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'
'''


PKGS_TO_INSTALL = [
    'zlib-devel',
    'bzip2',
    'bzip2-devel',
    'readline-devel',
    'sqlite',
    'sqlite-devel',
    'openssl-devel',
    'xz',
    'xz-devel',
    'libffi-devel',
    'python3-devel',
    'zsh',
    'util-linux-user',
    'golang',
    'powerline-fonts',
    'nvim',
    'kitty',
]


def _exc(cmd):
    """Excecute given cmd with subprocess. Return its returncode."""
    process = subprocess.run(shlex.split(cmd))
    returncode = process.returncode
    _tell('', stcode=returncode)
    return returncode


def _tell(msg, stcode=None):
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


def install_base_pkgs():
    _tell("Going to install base pkgs...")
    _exc(f"sudo dnf install -y {' '.join(pkg for pkg in PKGS_TO_INSTALL)}")


def install_vs_code():
    _tell("Going to install vscode...")
    _tell("Importing vscode repo...")
    _exc("sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc")
    _tell("Adding Microsoft vscode gpg key...")
    _exc(VSCODE_GPG_KEY_CMD)


def setup_zsh_shell():
    """Setup zsh for current user."""
    _tell("Going to setup zsh...")
    zshrc = f'{HOME}/.zshrc'
    if os.path.exists(zshrc):
        os.unlink(zshrc)

    ohmyzsh = f'{HOME}/.oh-my-zsh'
    if os.path.exists(ohmyzsh):
        shutil.rmtree(ohmyzsh)
    _tell("Downloading oh-my-zsh...")
    _exc(f"git clone git://github.com/robbyrussell/oh-my-zsh.git {ohmyzsh}")

    _tell("Setting oh-my-zsh base template as zshrc file...")
    _exc(f"cp {ohmyzsh}/templates/zshrc.zsh-template {HOME}/.zshrc")

    _tell("Changing user shell to zsh...")
    _exc("chsh -s /usr/bin/zsh")


def setup_kitty_term(theme=KITTY_TERMINAL_DEFAULT_THEME):
    """Setup kitty terminal."""
    kitty_dir = f"{HOME}/.config/kitty"
    kitty_conf = f"{HOME}/.config/kitty/kitty.conf"
    kitty_themes_dir = f"{kitty_dir}/kitty-themes"
    if not os.path.isdir(kitty_themes_dir):
        _tell("Going to download kitty themes...")
        _exc(f"git clone --depth 1 git@github.com:dexpota/kitty-themes.git {HOME}/.config/kitty/kitty-themes")
    _tell("Set kitty theme...")
    if os.path.isfile(f"{kitty_dir}/theme.conf"):
        _tell("Removing previous kitty theme...")
        os.unlink(f"{kitty_dir}/theme.conf")
    _exc(f"ln -s {kitty_dir}/kitty-themes/themes/{theme} {kitty_dir}/theme.conf")
    if not os.path.isfile(kitty_conf):
        _tell(f"Creating default {kitty_conf} file...")
        with open(kitty_conf, 'w') as fp:
            fp.write('include ./theme.conf')


def install_pyenv():
    _tell("Going to install pyenv")
    os.system("curl https://pyenv.run | bash")

    _tell("Configuring zsh PATH with pyenv")
    with open(f"{HOME}/.zshrc", "a") as zshrc:
        zshrc.write('\n')
        zshrc.write(f'export PATH="{HOME}/.pyenv/bin:$PATH"\n')
        zshrc.write('eval "$(pyenv init -)"\n')
        zshrc.write('eval "$(pyenv virtualenv-init -)"\n')


def setup_golang():
    gohome = f"{HOME}/Code/go"
    pathlib.Path(gohome).mkdir(parents=True, exist_ok=True)
    with open(f"{HOME}/.zshrc", "a") as zshrc:
        zshrc.write('\n')
        zshrc.write(f'export GOPATH="{gohome}"\n')


def install_fonts():
    _tell("Going to install Fira Code fonts...")
    os.system('bash ./fonts/install_fira_code.sh') 


def last_step():
    _tell("Dont forget to:")
    _tell("\t1- Change your user shell to zsh")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        _tell("Excecute:\n\tpython bootstrap.py restore\n")
        sys.exit(0)
    if sys.argv[1] == "restore":
        install_base_pkgs()
        install_fonts()
        setup_zsh_shell()
        install_vs_code()
        install_pyenv()
        last_step()