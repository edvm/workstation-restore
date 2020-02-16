# Elementary OS

from recipes.common import execute, tell_user, HOME, SCRIPT_PATH
from recipes.spaceship import install_spaceship_prompt
from recipes.ohmyzsh import setup_oh_my_zsh
from recipes.pyenv import install_pyenv 
from recipes.fonts import install_fonts
from recipes.node import setup_node_npm_n
from recipes.nvm import install_nvm

PKGS_TO_INSTALL = ["git", "zsh", "curl", "snapd", "python3-pip"]


def restore():
    """Restore my system. Install in order all fns"""

    # Base
    install_base_pkgs()
    setup_oh_my_zsh()
    install_node_npm()

    # Js
    install_spaceship_prompt()
    setup_node_npm_n()
    install_nvm()

    # Python
    install_pyenv()

    # Others
    install_fonts()
    install_spotify()
    install_vs_code()


def install_base_pkgs(pkgs=None):
    """Install basic system packages (dev headers, tools, lang compilers, etc.)"""
    if not pkgs:
        pkgs = PKGS_TO_INSTALL
    tell_user("Going to install base pkgs...")
    execute(f"sudo apt update")
    execute(f"sudo apt install -y {' '.join(pkg for pkg in pkgs)}")
    execute(f"sudo apt autoremove -y")


def install_vs_code():
    """Install vscode"""
    tell_user("Going to install base pkgs...")
    execute("sudo snap install code --classic")


def install_node_npm():
    """Install node npm."""
    tell_user("Going to install node and npm...")
    execute("sudo snap install node --edge --classic")
    from recipes.node import setup_node_npm_n

    tell_user("Setting up node and npm...")
    setup_node_npm_n()


def install_spotify():
    tell_user("Going to install spotify...")
    execute("sudo snap install spotify --classic")
