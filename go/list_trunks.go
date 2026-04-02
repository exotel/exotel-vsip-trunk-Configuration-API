package main

import (
	"fmt"
	"os"
)

func main() {
	fmt.Println("Listing trunks...")
	q := map[string]string{}
	if v := os.Getenv("PAGE_SIZE"); v != "" {
		q["page_size"] = v
	}
	if v := os.Getenv("PAGE_OFFSET"); v != "" {
		q["offset"] = v
	}
	if v := os.Getenv("TRUNK_SID"); v != "" {
		q["trunk_sid"] = v
	}
	get("/trunks", q)
}
