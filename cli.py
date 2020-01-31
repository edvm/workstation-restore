#!/usr/bin/env python

import os
import sys
import cmd
import dummy
import fedora
import inspect

from recipes.common import tell_user, SCRIPT_PATH


class SystemRestoreShell(cmd.Cmd):
    """System Restore Shell."""

    intro = "Welcome to System Restore. Type help or ? to list commands.\n"
    distro = ""
    distros = {"fedora": fedora, "dummy": dummy}

    to_remove = []
    system_restore_shell_cmds = ["help", "?", "change_distro", "quit"]

    @property
    def prompt(self):
        if self.distro:
            return f"({self.distro}-restore) "
        return "(set distro to use) "

    @property
    def current_distro_module(self):
        return self.distros[self.distro]

    def module_fns_list(self, module):
        """Return functions found in given module."""
        for member in inspect.getmembers(module):
            if inspect.isfunction(member[1]):
                yield member

    def remove_old_fns(self):
        """Remove previously loaded functions."""
        names = self.get_names()
        for fname in self.to_remove:
            if fname in names:
                try:
                    delattr(self.__class__, fname)
                except:  # Silently pass this exception (!Zen of Python)
                    pass

    def load_module_fns(self, module=fedora):
        """Load module functions."""
        self.remove_old_fns()
        for fname, fn in self.module_fns_list(module):
            if fname.startswith("_"):
                continue
            name = f"do_{fname}"
            self.to_remove.append(name)
            if name not in self.get_names():
                setattr(self.__class__, name, fn)

    def onecmd(self, line):
        """Interpret the argument as though it had been typed in response
        to the prompt.
        This may be overridden, but should not normally need to be;
        see the precmd() and postcmd() methods for useful execution hooks.
        The return value is a flag indicating whether interpretation of
        commands by the interpreter should stop.
        """
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if line == "EOF":
            self.lastcmd = ""
        if cmd == "":
            return self.default(line)
        else:
            try:
                if cmd in self.system_restore_shell_cmds:
                    func = getattr(self, "do_" + cmd)
                else:
                    func = getattr(self.current_distro_module, cmd)
                    if not arg:  # if no args defined, just call module `func` right now
                        return func()
            except AttributeError:
                return self.default(line)
            return func(arg)

    def do_change_distro(self, arg):
        """Change distro."""
        supported_distros = ["dummy", "fedora"]
        if arg not in supported_distros:
            tell_user(
                f"Sorry, {arg} is not supported\nSupported distros are: {supported_distros}",
                1,
            )
            return
        self.distro = arg
        os.system("clear")
        self.load_module_fns(self.distros[arg])

    def do_quit(self, arg):
        """Exit system restore."""
        return True


if __name__ == "__main__":
    # Insert path to this script to `sys.path`
    sys.path.insert(0, SCRIPT_PATH)
    SystemRestoreShell().cmdloop()
