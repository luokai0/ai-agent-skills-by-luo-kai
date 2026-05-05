BINARY_NAME=agentskills
VERSION=$(shell git describe --tags --always --dirty 2>/dev/null || echo "dev")

.PHONY: build build-linux build-darwin build-windows clean test

build:
	go build -ldflags "-X main.version=$(VERSION)" -o bin/$(BINARY_NAME) .

build-linux:
	GOOS=linux GOARCH=amd64 go build -ldflags "-X main.version=$(VERSION)" -o bin/$(BINARY_NAME)-linux-amd64 .

build-darwin:
	GOOS=darwin GOARCH=amd64 go build -ldflags "-X main.version=$(VERSION)" -o bin/$(BINARY_NAME)-darwin-amd64 .
	GOOS=darwin GOARCH=arm64 go build -ldflags "-X main.version=$(VERSION)" -o bin/$(BINARY_NAME)-darwin-arm64 .

build-windows:
	GOOS=windows GOARCH=amd64 go build -ldflags "-X main.version=$(VERSION)" -o bin/$(BINARY_NAME)-windows-amd64.exe .

clean:
	rm -rf bin/

test:
	go test ./...
