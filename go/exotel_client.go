package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
)

// base returns the base URL for Exotel API calls
func base() string {
	authKey := os.Getenv("EXO_AUTH_KEY")
	authToken := os.Getenv("EXO_AUTH_TOKEN")
	domain := os.Getenv("EXO_SUBSCRIBIX_DOMAIN")
	accountSid := os.Getenv("EXO_ACCOUNT_SID")

	if authKey == "" || authToken == "" || domain == "" || accountSid == "" {
		fmt.Println("Error: Missing required environment variables (EXO_AUTH_KEY, EXO_AUTH_TOKEN, EXO_SUBSCRIBIX_DOMAIN, EXO_ACCOUNT_SID)")
		os.Exit(1)
	}

	return fmt.Sprintf("https://%s:%s@%s/v2/accounts/%s", authKey, authToken, domain, accountSid)
}

// post makes a POST request to the Exotel API
func post(path string, payload interface{}) map[string]interface{} {
	b, err := json.Marshal(payload)
	if err != nil {
		fmt.Printf("Error marshaling JSON: %v\n", err)
		os.Exit(1)
	}

	req, err := http.NewRequest("POST", base()+path, bytes.NewReader(b))
	if err != nil {
		fmt.Printf("Error creating request: %v\n", err)
		os.Exit(1)
	}

	req.Header.Set("Content-Type", "application/json")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		fmt.Printf("Error making request: %v\n", err)
		os.Exit(1)
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("Error reading response: %v\n", err)
		os.Exit(1)
	}

	if resp.StatusCode >= 400 {
		fmt.Printf("HTTP Error %d: %s\n", resp.StatusCode, string(body))
		os.Exit(1)
	}

	fmt.Println(string(body))

	var out map[string]interface{}
	if err := json.Unmarshal(body, &out); err != nil {
		fmt.Printf("Error parsing JSON response: %v\n", err)
		os.Exit(1)
	}

	return out
}

func get(path string, query map[string]string) map[string]interface{} {
	u := base() + path
	if len(query) > 0 {
		q := url.Values{}
		for k, v := range query {
			if v != "" {
				q.Set(k, v)
			}
		}
		if enc := q.Encode(); enc != "" {
			u += "?" + enc
		}
	}
	req, err := http.NewRequest("GET", u, nil)
	if err != nil {
		fmt.Printf("Error creating request: %v\n", err)
		os.Exit(1)
	}
	return doJSON(req)
}

func put(path string, payload interface{}) map[string]interface{} {
	b, err := json.Marshal(payload)
	if err != nil {
		fmt.Printf("Error marshaling JSON: %v\n", err)
		os.Exit(1)
	}
	req, err := http.NewRequest("PUT", base()+path, bytes.NewReader(b))
	if err != nil {
		fmt.Printf("Error creating request: %v\n", err)
		os.Exit(1)
	}
	req.Header.Set("Content-Type", "application/json")
	return doJSON(req)
}

func deleteReq(path string, query map[string]string) map[string]interface{} {
	u := base() + path
	if len(query) > 0 {
		q := url.Values{}
		for k, v := range query {
			if v != "" {
				q.Set(k, v)
			}
		}
		if enc := q.Encode(); enc != "" {
			u += "?" + enc
		}
	}
	req, err := http.NewRequest("DELETE", u, nil)
	if err != nil {
		fmt.Printf("Error creating request: %v\n", err)
		os.Exit(1)
	}
	return doJSON(req)
}

func doJSON(req *http.Request) map[string]interface{} {
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		fmt.Printf("Error making request: %v\n", err)
		os.Exit(1)
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("Error reading response: %v\n", err)
		os.Exit(1)
	}
	if resp.StatusCode >= 400 {
		fmt.Printf("HTTP Error %d: %s\n", resp.StatusCode, string(body))
		os.Exit(1)
	}
	fmt.Println(string(body))
	var out map[string]interface{}
	if err := json.Unmarshal(body, &out); err != nil {
		fmt.Printf("Error parsing JSON: %v\n", err)
		os.Exit(1)
	}
	return out
}

// getenvDefault returns the environment variable value or a default
func getenvDefault(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}
