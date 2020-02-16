# Install NVM.

import os
from recipes.common import tell_user, HOME

def install_nvm():
    """Install nvm."""
    tell_user("Going to install nvm")
    os.system("curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.2/install.sh | bash")

