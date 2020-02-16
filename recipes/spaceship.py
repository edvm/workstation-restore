from recipes.common import execute, tell_user


def install_spaceship_prompt():
    """Install spaceship prompt.
    https://github.com/denysdovhan/spaceship-prompt

    NOTE: Be sure to have `node`/`npm` installed on your system 
    """
    execute("npm i -g spaceship-prompt")
