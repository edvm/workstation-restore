package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"strings"
)

const vscodeGpgKeyCmd string = `sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'`

var pkgsToInstall = [...]string{
	"zlib-devel",
	"bzip2",
	"bzip2-devel",
	"readline-devel",
	"sqlite",
	"sqlite-devel",
	"openssl-devel",
	"xz",
	"xz-devel",
	"libffi-devel",
	"python3-devel",
	"zsh",
	"util-linux-user",
	"golang",
}

type command struct {
	Dry  bool
	Name string
	Args string
}

func run(command command) {
	if command.Dry == true {
		fmt.Println("DRY :: Should excecute:\n\t", command.Name, command.Args)
		return
	}
	cmd := exec.Command(command.Name, strings.Split(command.Args, " ")...)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err := cmd.Run()
	if err != nil {
		log.Fatalf("cmd.Run() failed with %s\n", err)
	}
}

func testCmd() {
	cmd := command{
		Name: "ls",
		Args: "-l -a -s",
	}
	run(cmd)
}

func installPkgs() {
	cmd := command{
		Name: "sudo",
		Args: "dnf install -y " + strings.Join(pkgsToInstall[:], " "),
	}
	run(cmd)
}

func main() {
	testCmd()
	installPkgs()
}
