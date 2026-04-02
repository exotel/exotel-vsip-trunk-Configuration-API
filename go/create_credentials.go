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
	pass := os.Getenv("SIP_CRED_PASSWORD")
	if pass == "" {
		fmt.Println("Error: SIP_CRED_PASSWORD required")
		os.Exit(1)
	}
	body := map[string]string{
		"user_name":     getenvDefault("SIP_CRED_USERNAME", "voice_ai_user"),
		"password":      pass,
		"friendly_name": getenvDefault("SIP_CRED_FRIENDLY_NAME", "streamkit"),
	}
	fmt.Println("Creating SIP credentials...")
	post("/trunks/"+trunk+"/credentials", body)
}
