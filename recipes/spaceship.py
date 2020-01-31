from recipes.common import execute


def install_spaceship_prompt():
    """Install spaceship prompt.
    https://github.com/denysdovhan/spaceship-prompt
    NOTE: Be sure to execute `setup_node_npm_n` before.
    """
    i = input("Have you executed `setup_node_npm_n` before? (y/n)")
    if i == "n":
        from recipes.node import setup_node_npm_n
        setup_node_npm_n()
    execute("npm i -g spaceship-prompt")
