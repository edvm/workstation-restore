import os
import shutil

from recipes.common import tell_user, execute


HOME = os.getenv("HOME")


def setup_oh_my_zsh(change_usershell=False):
    """Download and setup `oh my zsh` for current user.

    Arguments:

        - change_usershell (bool)   If True, it will execute `chsh` to set users shell to zsh
    """

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

    if change_usershell:
        tell_user("Changing user shell to zsh...")
        execute("chsh -s /usr/bin/zsh")
