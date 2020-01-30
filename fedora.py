import pathlib
import shutil
import sys
import cmd
import os

from common import execute, tell_user

HOME = os.getenv("HOME")
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
KITTY_TERMINAL_DEFAULT_THEME = "Argonaut.conf"  # default kitty term name

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


def install_base_pkgs(cmd, pkgs=None):
    """Install basic system packages (dev headers, tools, lang compilers, etc.)"""
    if not pkgs:
        pkgs = PKGS_TO_INSTALL
    tell_user("Going to install base pkgs...")
    execute(f"sudo dnf install -y {' '.join(pkg for pkg in pkgs)}")


def install_vs_code(cmd):
    """Import Microsoft vscode gpg key, adds microsoft repository and then install vscode."""
    tell_user("Going to install vscode...")
    tell_user("Importing vscode repo...")
    execute("sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc")
    tell_user("Adding Microsoft vscode gpg key...")
    execute(VSCODE_GPG_KEY_CMD)
    tell_user("Going to install vscode...")
    execute("sudo dnf install -y code")


def setup_zsh_shell(cmd):
    """Setup zsh for current user."""
    tell_user("Going to setup zsh...")
    zshrc = f"{HOME}/.zshrc"
    if os.path.exists(zshrc):
        os.unlink(zshrc)

    ohmyzsh = f"{HOME}/.oh-my-zsh"
    if os.path.exists(ohmyzsh):
        shutil.rmtree(ohmyzsh)
    tell_user("Downloading oh-my-zsh...")
    execute(f"git clone git://github.com/robbyrussell/oh-my-zsh.git {ohmyzsh}")

    tell_user("Setting oh-my-zsh base template as zshrc file...")
    execute(f"cp {ohmyzsh}/templates/zshrc.zsh-template {HOME}/.zshrc")

    tell_user("Changing user shell to zsh...")
    execute("chsh -s /usr/bin/zsh")


def setup_kitty_term(theme=KITTY_TERMINAL_DEFAULT_THEME):
    """Setup kitty terminal."""
    kitty_dir = f"{HOME}/.config/kitty"
    kitty_conf = f"{HOME}/.config/kitty/kitty.conf"
    kitty_themes_dir = f"{kitty_dir}/kitty-themes"
    if not os.path.isdir(kitty_themes_dir):
        tell_user("Going to download kitty themes...")
        execute(
            f"git clone --depth 1 git@github.com:dexpota/kitty-themes.git {HOME}/.config/kitty/kitty-themes"
        )
    tell_user("Set kitty theme...")
    if os.path.isfile(f"{kitty_dir}/theme.conf"):
        tell_user("Removing previous kitty theme...")
        os.unlink(f"{kitty_dir}/theme.conf")
    execute(f"ln -s {kitty_dir}/kitty-themes/themes/{theme} {kitty_dir}/theme.conf")
    if not os.path.isfile(kitty_conf):
        tell_user(f"Creating default {kitty_conf} file...")
        shutil.copyfile(f"{SCRIPT_PATH}/kitty/kitty.conf", kitty_conf)


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


def setup_node_npm_n():
    """Setup npm package dir and install/configure `n`..."""
    tell_user("Create a directory for global npm packages...")
    npm_packages_dir = f"{HOME}/.local/node/npm-packages"
    pathlib.Path(npm_packages_dir).mkdir(parents=True, exist_ok=True)

    tell_user("Tell `npm` where to store globally installed packages...")
    execute(f"npm config set prefix {npm_packages_dir}")

    tell_user("Create a directory for global node versions...")
    n_dir = f"{HOME}/.local/node/n"
    pathlib.Path(n_dir).mkdir(parents=True, exist_ok=True)

    tell_user("Ensure `npm` will find installed binaries and man packages")
    zshrc = f"{HOME}/.zshrc"
    with open(zshrc, "a") as fp:
        fp.write("\n")
        fp.write("# Fedora restore :: setup node to install packages without sudo\n")
        fp.write(f'export NPM_PACKAGES="{npm_packages_dir}"\n')
        fp.write(f'export N_PREFIX="{n_dir}"\n')
        fp.write('export PATH="$PATH:$NPM_PACKAGES/bin"\n')
        fp.write('export MANPATH="${MANPATH-$(manpath)}:$NPM_PACKAGES/share/man"\n')

    execute(f"npm i -g n", env={"NPM_PACKAGES": npm_packages_dir})


def install_pyenv():
    tell_user("Going to install pyenv")
    os.system("curl https://pyenv.run | bash")

    tell_user("Configuring zsh PATH with pyenv")
    with open(f"{HOME}/.zshrc", "a") as zshrc:
        zshrc.write("\n")
        zshrc.write("# Fedora restore :: pyenv\n")
        zshrc.write(f'export PATH="{HOME}/.pyenv/bin:$PATH"\n')
        zshrc.write('eval "$(pyenv init -)"\n')
        zshrc.write('eval "$(pyenv virtualenv-init -)"\n')


def install_spaceship_prompt():
    """Install spaceship prompt.
    https://github.com/denysdovhan/spaceship-prompt
    NOTE: Be sure to execute `setup_node_npm_n` before.
    """
    i = input("Have you executed `setup_node_npm_n` before? (y/n)")
    if i == "n":
        setup_node_npm_n()
    execute("npm i -g spaceship-prompt")


def setup_golang():
    gohome = f"{HOME}/Code/go"
    pathlib.Path(gohome).mkdir(parents=True, exist_ok=True)
    with open(f"{HOME}/.zshrc", "a") as zshrc:
        zshrc.write("\n")
        zshrc.write("# Fedora restore :: setup GOHOME\n")
        zshrc.write(f'export GOPATH="{gohome}"\n')


def install_fonts():
    tell_user("Going to install Fira Code fonts...")
    os.system("bash ./fonts/install_fira_code.sh")

