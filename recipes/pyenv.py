import os

from recipes.common import tell_user, HOME


def install_pyenv(configure_zsh=False):
    """Install pyenv.

    Arguments:

        - configure_zsh (bool)  Defaults False, if True it will update `~/.zshrc` file
                                with `pyenv` config.
    
    """
    tell_user("Going to install pyenv")
    os.system("curl https://pyenv.run | bash")

    zshrc = f"{HOME}/.zshrc"
    if not os.path.isfile(zshrc):
        return

    tell_user("Configuring zsh PATH with pyenv")
    with open(zshrc, "a") as fp:
        fp.write("\n")
        fp.write("# Fedora restore :: pyenv\n")
        fp.write(f'export PATH="{HOME}/.pyenv/bin:$PATH"\n')
        fp.write('eval "$(pyenv init -)"\n')
        fp.write('eval "$(pyenv virtualenv-init -)"\n')
