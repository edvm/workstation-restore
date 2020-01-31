import pathlib
import shutil
import sys
import os

from recipes.common import execute, tell_user, HOME, SCRIPT_PATH
from recipes.zsh import setup_zsh_shell
from recipes.pyenv import install_pyenv
from recipes.kitty import setup_kitty_term
from recipes.node import setup_node_npm_n
from recipes.spaceship import install_spaceship_prompt
from recipes.fonts import install_fonts


VSCODE_GPG_KEY_CMD = """
sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'
"""

PKGS_TO_INSTALL = [
    "zlib-devel",
    "bzip2",
    "bzip2-devel",
    "readline-devel",
    "sqlite",
    "sqlite-devel",
    "openssl-devel",
    "xz",
    "xz-devel",
    "libffi-devel",
    "python3-devel",
    "zsh",
    "util-linux-user",
    "golang",
    "powerline-fonts",
    "nvim",
    "kitty",
    "flameshot",
    "npm",
    "libpq-devel",
]


def install_base_pkgs(pkgs=None):
    """Install basic system packages (dev headers, tools, lang compilers, etc.)"""
    if not pkgs:
        pkgs = PKGS_TO_INSTALL
    tell_user("Going to install base pkgs...")
    execute(f"sudo dnf install -y {' '.join(pkg for pkg in pkgs)}")


def install_vs_code():
    """Import Microsoft vscode gpg key, adds microsoft repository and then install vscode."""
    tell_user("Going to install vscode...")
    tell_user("Importing vscode repo...")
    execute("sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc")
    tell_user("Adding Microsoft vscode gpg key...")
    execute(VSCODE_GPG_KEY_CMD)
    tell_user("Going to install vscode...")
    execute("sudo dnf install -y code")


def setup_fisa_vim():
    """Setup fisa vim."""
    tell_user("Going to install fisa vim deps...")
    fisa_requirements = [
        "ctags-etags",
        "python3-flake8",
        "python3-pylint",
        "python3-isort",
    ]
    execute(f"sudo dnf install -y {' '.join(pkg for pkg in fisa_requirements)}")
    execute("pip3 install --user pynvim")

    nvim_dir = f"{HOME}/.config/nvim"
    tell_user("Downloading fisa vim config...")
    if not os.path.isdir(f"{nvim_dir}"):
        os.makedirs(f"{nvim_dir}")
    execute(
        f"wget -O {nvim_dir}/init.vim https://raw.github.com/fisadev/fisa-vim-config/master/config.vim"
    )


def setup_golang():
    gohome = f"{HOME}/Code/go"
    pathlib.Path(gohome).mkdir(parents=True, exist_ok=True)
    with open(f"{HOME}/.zshrc", "a") as zshrc:
        zshrc.write("\n")
        zshrc.write("# Fedora restore :: setup GOHOME\n")
        zshrc.write(f'export GOPATH="{gohome}"\n')
        zshrc.write(f'export GO111MODULE="auto"\n')
