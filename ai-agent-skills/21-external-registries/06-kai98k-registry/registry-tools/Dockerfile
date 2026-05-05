# === Build Stage ===
FROM golang:1.24-alpine AS builder
RUN apk add --no-cache git
ENV GOTOOLCHAIN=local
WORKDIR /src
COPY cli/go.mod cli/go.sum ./
RUN go mod download
COPY cli/ .
RUN CGO_ENABLED=0 go build -tags server -ldflags="-s -w" -o /agentskills-server .

# === Runtime Stage (~25MB) ===
FROM alpine:3.19
RUN apk add --no-cache ca-certificates tzdata
COPY --from=builder /agentskills-server /usr/local/bin/agentskills-server
RUN mkdir -p /data/bundles
VOLUME ["/data"]
EXPOSE 8000
ENTRYPOINT ["agentskills-server"]
CMD ["serve", "--port", "8000"]
