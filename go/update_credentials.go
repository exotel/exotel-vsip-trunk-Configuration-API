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
	body := map[string]string{}
	if v := os.Getenv("SIP_CRED_FRIENDLY_NAME"); v != "" {
		body["friendly_name"] = v
	}
	if v := os.Getenv("SIP_CRED_USERNAME"); v != "" {
		body["user_name"] = v
	}
	if v := os.Getenv("SIP_CRED_PASSWORD"); v != "" {
		body["password"] = v
	}
	if len(body) == 0 {
		body["friendly_name"] = "updated_label"
	}
	fmt.Println("Updating credential...")
	put("/trunks/"+trunk+"/credentials/"+cid, body)
}
