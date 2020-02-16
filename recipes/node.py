import pathlib

from recipes.common import HOME, tell_user, execute


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
        fp.write("# Setup node to install packages without sudo\n")
        fp.write(f'export NPM_PACKAGES="{npm_packages_dir}"\n')
        fp.write(f'export N_PREFIX="{n_dir}"\n')
        fp.write('export PATH="$PATH:$NPM_PACKAGES/bin"\n')
        fp.write('export MANPATH="${MANPATH-$(manpath)}:$NPM_PACKAGES/share/man"\n')

    execute(f"npm i -g n", env={"NPM_PACKAGES": npm_packages_dir})
