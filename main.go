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

func run(cmdName string, cmdArgs []string, dry bool) {
	if dry == true {
		fmt.Println("DRY :: Should excecute:\n\t", cmdName, strings.Join(cmdArgs[:], " "))
		return
	}
	cmd := exec.Command(cmdName, cmdArgs...)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err := cmd.Run()
	if err != nil {
		log.Fatalf("cmd.Run() failed with %s\n", err)
	}
}

func testCmd() {
	cmdName := "ls"
	cmdArgs := []string{"-l", "-a", "-s"}
	run(cmdName, cmdArgs, true)
}

func installPkgs() {
	cmdName := "sudo dnf"
	cmdArgs := []string{"install", "-y", strings.Join(pkgsToInstall[:], " ")}
	run(cmdName, cmdArgs, true)
}

func main() {
	// fmt.Println(vscodeGpgKeyCmd)
	// fmt.Println(pkgsToInstall)
	// testCmd()
	installPkgs()
}
