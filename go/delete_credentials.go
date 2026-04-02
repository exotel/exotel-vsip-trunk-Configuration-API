package main

import (
	"fmt"
	"os"
)

func main() {
	trunk := os.Getenv("TRUNK_SID")
	cid := os.Getenv("CREDENTIAL_ID")
	if trunk == "" || cid == "" {
		fmt.Println("Error: TRUNK_SID and CREDENTIAL_ID required")
		os.Exit(1)
	}
	fmt.Println("Deleting credential...")
	deleteReq("/trunks/"+trunk+"/credentials", map[string]string{"id": cid})
}
