package main

import (
	"fmt"
	"os"
)

func main() {
	ex := os.Getenv("EXOPHONE")
	if ex == "" {
		ex = os.Getenv("DID_NUMBER")
	}
	if ex == "" {
		fmt.Println("Error: set EXOPHONE or DID_NUMBER")
		os.Exit(1)
	}
	q := map[string]string{"exophone": ex}
	if v := os.Getenv("TRUNK_SID"); v != "" {
		q["trunk_sid"] = v
	}
	fmt.Println("Trunk map lookup...")
	get("/trunk-maps", q)
}
