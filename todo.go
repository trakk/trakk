package main

import (
	"bufio"
	"fmt"
	"os"
)

func PrintOps() {
	fmt.Printf("What would you like to do?\n")
	fmt.Printf("'x' to exit\n")
}

func main() {
	input := ""
	reader := bufio.NewReader(os.Stdin)
	
	fmt.Printf("you have a lot of stuff to do\n")
	for input != "x\n" {
		PrintOps()
		
		text, _ := reader.ReadString('\n')
		input = text
	}
	
	fmt.Printf("Now get to work, slacker!\n")
}