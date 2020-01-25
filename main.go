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

func check(e error) {
	if e != nil {
		panic(e)
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
	fmt.Println("Going to install base packages...")
	cmd := command{
		Name: "sudo",
		Args: "dnf install -y " + strings.Join(pkgsToInstall[:], " "),
	}
	run(cmd)
}

func installFonts() {
	fmt.Println("Going to install Fira Code fonts...")
	cmd := command{
		Name: "sudo",
		Args: "bash ./fonts/install_fira_code.sh",
	}
	run(cmd)
}

func setupGolang() {
	goDir := os.Getenv("HOME") + "/Code/go"
	_, error := os.Stat(goDir)
	if error != nil {
		if os.IsNotExist(error) {
			fmt.Println("Go dir doesnt exists at: ", goDir)
		}
	} else {
		fmt.Println("Found go dir at:", goDir)
	}
	fmt.Println("Going to setup golang...")

	zshrc := os.Getenv("HOME") + "/.zshrc"
	f, err := os.OpenFile(zshrc, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	check(err)
	defer f.Close()

	if _, err := f.Write([]byte("\nexport GOPATH=\"" + goDir + "\"\n")); err != nil {
		check(err)
	}
}

func main() {
	// testCmd()
	// installPkgs()
	// installFonts()
	setupGolang()
}
