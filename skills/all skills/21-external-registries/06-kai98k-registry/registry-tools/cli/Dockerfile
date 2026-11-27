FROM golang:1.24-alpine AS builder

RUN apk add --no-cache git

WORKDIR /app

# Copy go.mod and go.sum first for better Docker layer caching
COPY go.mod go.sum ./
ENV GOTOOLCHAIN=local
RUN go mod download

# Copy source code and build
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /agentskills .

FROM alpine:3.20

RUN apk add --no-cache ca-certificates
COPY --from=builder /agentskills /usr/local/bin/agentskills

ENTRYPOINT ["agentskills"]
