package main

import (
    "fmt"
    "os"
)

func main() {
    trunkSid := os.Getenv("TRUNK_SID")
    if trunkSid == "" {
        fmt.Println("Error: TRUNK_SID environment variable is required")
        os.Exit(1)
    }

    fmt.Printf("Getting credentials for trunk %s...\n", trunkSid)
    result := get(fmt.Sprintf("/trunks/%s/credentials", trunkSid))
    fmt.Println("Credentials retrieved successfully!")
    _ = result
} 