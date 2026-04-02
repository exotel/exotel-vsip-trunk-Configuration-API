# Go samples

Load environment from the repository root (copy `.env.example` → `.env` there).

Run **`exotel_client.go`** together with the operation you want:

```bash
cd go
go run exotel_client.go list_trunks.go
go run exotel_client.go create_credentials.go
```

`exotel_client.go` defines the HTTP helpers; each other file is a small `main` package entrypoint.
