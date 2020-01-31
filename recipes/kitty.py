import os
import shutil

from recipes.common import HOME, SCRIPT_PATH, tell_user, execute

KITTY_TERMINAL_DEFAULT_THEME = "Argonaut.conf"  # default kitty term name


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
