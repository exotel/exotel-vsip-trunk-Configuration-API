package main

import (
	"fmt"
	"os"
)

func main() {
	trunk := os.Getenv("TRUNK_SID")
	if trunk == "" {
		fmt.Println("Error: TRUNK_SID required")
		os.Exit(1)
	}
	q := map[string]string{}
	if v := os.Getenv("PAGE_SIZE"); v != "" {
		q["page_size"] = v
	}
	if v := os.Getenv("PAGE_OFFSET"); v != "" {
		q["offset"] = v
	}
	if v := os.Getenv("CREDENTIAL_ID"); v != "" {
		q["id"] = v
	}
	fmt.Println("Listing credentials...")
	get("/trunks/"+trunk+"/credentials", q)
}
