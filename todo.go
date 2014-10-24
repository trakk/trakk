//     Simple DB-backed command line todo-list with recurring tasks, sub-task checklists, and stats.
//     Copyright (C) 2014  David Ulrich
// 
//     This program is free software: you can redistribute it and/or modify
//     it under the terms of the GNU Affero General Public License as published
//     by the Free Software Foundation, either version 3 of the License, or
//     (at your option) any later version.
// 
//     This program is distributed in the hope that it will be useful,
//     but WITHOUT ANY WARRANTY; without even the implied warranty of
//     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//     GNU Affero General Public License for more details.
// 
//     You should have received a copy of the GNU Affero General Public License
//     along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
