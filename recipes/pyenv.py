import os

from recipes.common import tell_user, HOME


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
