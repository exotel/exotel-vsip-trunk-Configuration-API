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

    fmt.Printf("Deleting trunk %s...\n", trunkSid)
    result := delete(fmt.Sprintf("/trunks?trunk_sid=%s", trunkSid))
    fmt.Println("Trunk deleted successfully!")
    _ = result
} 