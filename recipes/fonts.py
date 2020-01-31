import os

from recipes.common import tell_user, SCRIPT_PATH 


def install_fonts():
    tell_user("Going to install Fira Code fonts...")
    os.system(f"bash {SCRIPT_PATH}/fonts/install_fira_code.sh")