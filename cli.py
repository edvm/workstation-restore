#!/usr/bin/env python

import cmd


class SystemRestoreShell(cmd.Cmd):
    intro = "Welcome to Fedora System Restore. Type help or ? to list commands.\n"
    prompt = "(fedora-restore) "
    file = None

    def do_install_base_pkgs(self, arg):
        """Install base package system (dev header files, etc)."""

    def do_install_fonts(self, arg):
        """Install Fira Code fonts, and others..."""

    def do_setup_zsh_shell(self, arg):
        """Setup oh-my-zsh and zsh as the user shell."""

    def do_install_vs_code(self, arg):
        """Install vscode repo."""

    def do_install_pyenv(self, arg):
        """Install pyenv and configure it."""

    def do_setup_kitty_term(self, arg):
        """Install kitty term and configure it."""

    def do_setup_golang(self, arg):
        """Setup golang."""

    def do_setup_fisa_vim(self, arg):
        """Setup fisa vim."""

    def do_setup_npm(self, arg):
        """Setup npm."""


if __name__ == '__main__':
    SystemRestoreShell().cmdloop()