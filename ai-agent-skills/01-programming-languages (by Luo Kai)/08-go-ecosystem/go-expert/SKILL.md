---
author: luo-kai
name: go-expert
description: Expert-level Go programming. Use when writing Go code, working with goroutines, channels, interfaces, error handling patterns, Go modules, testing, benchmarking, or building Go services and CLIs. Also use when the user mentions 'goroutine', 'channel', 'defer', 'interface', 'go test', 'go mod', 'context', 'panic/recover', or 'Go compile error'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Go Expert

You are an expert Go engineer with deep knowledge of Go idioms, concurrency patterns, the standard library, and building production Go services.

## Before Starting

1. **Service type** — HTTP API, CLI, background worker, library, microservice?
2. **Go version** — 1.21, 1.22, 1.23? (generics, slices package, log/slog available?)
3. **Framework** — bare net/http, Chi, Gin, Echo, Fiber?
4. **Database** — database/sql, sqlx, GORM, sqlc, pgx?
5. **Problem type** — writing code, debugging, performance, concurrency issue?

---

## Core Expertise Areas

- **Goroutines & channels**: fan-out/fan-in, worker pools, done channels, select
- **Interfaces**: small interfaces, structural typing, io.Reader/Writer, dependency injection
- **Error handling**: sentinel errors, error types, errors.Is/As, wrapping with %w
- **Context**: cancellation, deadlines, values, propagation through call chain
- **Standard library**: net/http, encoding/json, database/sql, sync, os, io
- **Testing**: table-driven tests, testify, httptest, mocking with interfaces
- **Performance**: profiling with pprof, escape analysis, memory allocation reduction
- **Modules**: go.mod, go.sum, versioning, workspace, private modules

---

## Key Patterns & Code

### Project Structure
```
myservice/
  cmd/
    server/
      main.go         # entry point — thin, just wires everything together
    worker/
      main.go
  internal/           # private packages — not importable by external code
    handler/
      user.go
      user_test.go
    service/
      user.go
      user_test.go
    repository/
      user.go
      user_test.go
    model/
      user.go
  pkg/                # public packages — importable by external code
    middleware/
      auth.go
      logging.go
    validator/
      validator.go
  migrations/
    001_create_users.sql
  go.mod
  go.sum
  Makefile
```

### Interfaces — Small and Focused
```go
package main

import (
    "context"
    "io"
)

// Go proverb: the bigger the interface, the weaker the abstraction
// Keep interfaces small — 1 to 3 methods is ideal

// Bad — too large, hard to mock
type UserRepository interface {
    Create(ctx context.Context, user *User) error
    Update(ctx context.Context, user *User) error
    Delete(ctx context.Context, id int64) error
    FindByID(ctx context.Context, id int64) (*User, error)
    FindByEmail(ctx context.Context, email string) (*User, error)
    FindAll(ctx context.Context, limit, offset int) ([]*User, error)
    Count(ctx context.Context) (int64, error)
}

// Better — split by use case
type UserFinder interface {
    FindByID(ctx context.Context, id int64) (*User, error)
}

type UserCreator interface {
    Create(ctx context.Context, user *User) error
}

type UserWriter interface {
    Create(ctx context.Context, user *User) error
    Update(ctx context.Context, user *User) error
    Delete(ctx context.Context, id int64) error
}

// Accept interfaces, return concrete types (Go best practice)
type UserService struct {
    repo UserFinder  // only depends on what it needs
    log  *slog.Logger
}

func NewUserService(repo UserFinder, log *slog.Logger) *UserService {
    return &UserService{repo: repo, log: log}
}

// Standard library interfaces to know and use
type Stringer interface { String() string }             // fmt.Stringer
type Reader  interface { Read(p []byte) (n int, err error) }  // io.Reader
type Writer  interface { Write(p []byte) (n int, err error) } // io.Writer
type Closer  interface { Close() error }                // io.Closer
```

### Error Handling
```go
package main

import (
    "errors"
    "fmt"
)

// Sentinel errors — compare with errors.Is
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
    ErrConflict     = errors.New("conflict")
)

// Custom error type — use when you need fields
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error on field %q: %s", e.Field, e.Message)
}

// Wrap errors with %w to preserve chain
func loadUser(id int64) (*User, error) {
    user, err := db.QueryUser(id)
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            return nil, fmt.Errorf("loadUser(%d): %w", id, ErrNotFound)
        }
        return nil, fmt.Errorf("loadUser(%d): %w", id, err)
    }
    return user, nil
}

// Check errors with errors.Is and errors.As
func handleError(err error) {
    // Check sentinel error (works through wrap chain)
    if errors.Is(err, ErrNotFound) {
        fmt.Println("Resource not found")
        return
    }

    // Check error type (works through wrap chain)
    var valErr *ValidationError
    if errors.As(err, &valErr) {
        fmt.Printf("Invalid field %s: %s
", valErr.Field, valErr.Message)
        return
    }

    fmt.Printf("Unexpected error: %v
", err)
}

// Multiple return values — Go's idiomatic error handling
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("divide: division by zero")
    }
    return a / b, nil
}
```

### Goroutines & Channels
```go
package main

import (
    "context"
    "fmt"
    "sync"
)

// Worker pool pattern
func workerPool(ctx context.Context, jobs <-chan Job, numWorkers int) <-chan Result {
    results := make(chan Result, numWorkers)
    var wg sync.WaitGroup

    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                select {
                case <-ctx.Done():
                    return
                case results <- processJob(job):
                }
            }
        }()
    }

    // Close results when all workers done
    go func() {
        wg.Wait()
        close(results)
    }()

    return results
}

// Fan-out / fan-in
func fanOut(ctx context.Context, input <-chan int, numWorkers int) []<-chan int {
    channels := make([]<-chan int, numWorkers)
    for i := range channels {
        ch := make(chan int)
        channels[i] = ch
        go func(out chan<- int) {
            defer close(out)
            for v := range input {
                select {
                case out <- v * v:
                case <-ctx.Done():
                    return
                }
            }
        }(ch)
    }
    return channels
}

// Pipeline pattern
func generate(nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for _, n := range nums {
            out <- n
        }
    }()
    return out
}

func square(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in {
            out <- n * n
        }
    }()
    return out
}

// Done channel for cancellation (pre-context pattern, still useful)
func processUntilDone(done <-chan struct{}, items []string) {
    for _, item := range items {
        select {
        case <-done:
            fmt.Println("Stopping early")
            return
        default:
            process(item)
        }
    }
}
```

### Context — Proper Usage
```go
package main

import (
    "context"
    "time"
)

// Always pass context as first parameter
func fetchUser(ctx context.Context, id int64) (*User, error) {
    // Pass context to database query
    row := db.QueryRowContext(ctx,
        "SELECT id, name, email FROM users WHERE id = $1", id)

    var user User
    if err := row.Scan(&user.ID, &user.Name, &user.Email); err != nil {
        return nil, fmt.Errorf("fetchUser: %w", err)
    }
    return &user, nil
}

// HTTP handler — context carries deadline and cancellation
func userHandler(w http.ResponseWriter, r *http.Request) {
    // r.Context() is cancelled when client disconnects
    ctx := r.Context()

    // Add timeout to database operations
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel() // always call cancel to free resources

    user, err := fetchUser(ctx, getUserID(r))
    if err != nil {
        if errors.Is(err, context.DeadlineExceeded) {
            http.Error(w, "Request timeout", http.StatusGatewayTimeout)
            return
        }
        http.Error(w, "Internal error", http.StatusInternalServerError)
        return
    }

    json.NewEncoder(w).Encode(user)
}

// Context values — use typed keys to avoid collisions
type contextKey string

const (
    requestIDKey contextKey = "requestID"
    userIDKey    contextKey = "userID"
)

func withRequestID(ctx context.Context, id string) context.Context {
    return context.WithValue(ctx, requestIDKey, id)
}

func getRequestID(ctx context.Context) string {
    id, _ := ctx.Value(requestIDKey).(string)
    return id
}
```

### HTTP Server — Production Pattern
```go
package main

import (
    "context"
    "encoding/json"
    "log/slog"
    "net/http"
    "os"
    "os/signal"
    "syscall"
    "time"
)

type Server struct {
    router *http.ServeMux
    log    *slog.Logger
    db     *sql.DB
}

func NewServer(log *slog.Logger, db *sql.DB) *Server {
    s := &Server{
        router: http.NewServeMux(),
        log:    log,
        db:     db,
    }
    s.routes()
    return s
}

func (s *Server) routes() {
    s.router.HandleFunc("GET /health", s.handleHealth)
    s.router.HandleFunc("GET /api/users/{id}", s.handleGetUser)
    s.router.HandleFunc("POST /api/users", s.handleCreateUser)
}

func (s *Server) handleHealth(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
}

func (s *Server) handleGetUser(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")  // Go 1.22+ pattern matching

    user, err := s.getUser(r.Context(), id)
    if err != nil {
        s.respondError(w, err)
        return
    }

    s.respondJSON(w, http.StatusOK, user)
}

func (s *Server) respondJSON(w http.ResponseWriter, status int, data any) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    if err := json.NewEncoder(w).Encode(data); err != nil {
        s.log.Error("Failed to encode response", "error", err)
    }
}

func (s *Server) respondError(w http.ResponseWriter, err error) {
    var status int
    var message string

    switch {
    case errors.Is(err, ErrNotFound):
        status, message = http.StatusNotFound, "Not found"
    case errors.Is(err, ErrUnauthorized):
        status, message = http.StatusUnauthorized, "Unauthorized"
    default:
        s.log.Error("Unexpected error", "error", err)
        status, message = http.StatusInternalServerError, "Internal server error"
    }

    s.respondJSON(w, status, map[string]string{"error": message})
}

// Graceful shutdown
func main() {
    log := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
        Level: slog.LevelInfo,
    }))

    srv := &http.Server{
        Addr:         ":8080",
        Handler:      server.router,
        ReadTimeout:  10 * time.Second,
        WriteTimeout: 30 * time.Second,
        IdleTimeout:  120 * time.Second,
    }

    // Start server in goroutine
    go func() {
        log.Info("Server starting", "addr", srv.Addr)
        if err := srv.ListenAndServe(); err != http.ErrServerClosed {
            log.Error("Server failed", "error", err)
            os.Exit(1)
        }
    }()

    // Wait for interrupt signal
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    log.Info("Shutting down...")
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    if err := srv.Shutdown(ctx); err != nil {
        log.Error("Forced shutdown", "error", err)
    }

    log.Info("Server stopped")
}
```

### Table-Driven Tests
```go
package handler_test

import (
    "net/http"
    "net/http/httptest"
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestGetUser(t *testing.T) {
    tests := []struct {
        name       string
        userID     string
        mockUser   *User
        mockErr    error
        wantStatus int
        wantBody   string
    }{
        {
            name:       "valid user",
            userID:     "123",
            mockUser:   &User{ID: 123, Name: "Alice", Email: "alice@example.com"},
            wantStatus: http.StatusOK,
            wantBody:   `"name":"Alice"`,
        },
        {
            name:       "user not found",
            userID:     "999",
            mockErr:    ErrNotFound,
            wantStatus: http.StatusNotFound,
            wantBody:   `"error":"Not found"`,
        },
        {
            name:       "invalid id",
            userID:     "abc",
            wantStatus: http.StatusBadRequest,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // Setup mock
            mockRepo := &MockUserRepository{}
            if tt.mockUser != nil || tt.mockErr != nil {
                mockRepo.On("FindByID", mock.Anything, mock.Anything).
                    Return(tt.mockUser, tt.mockErr)
            }

            // Create handler
            handler := NewUserHandler(mockRepo)

            // Execute request
            req := httptest.NewRequest("GET", "/api/users/"+tt.userID, nil)
            rec := httptest.NewRecorder()
            handler.GetUser(rec, req)

            // Assert
            assert.Equal(t, tt.wantStatus, rec.Code)
            if tt.wantBody != "" {
                assert.Contains(t, rec.Body.String(), tt.wantBody)
            }
        })
    }
}
```

### Structured Logging with slog (Go 1.21+)
```go
import "log/slog"

// Setup structured JSON logger
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level:     slog.LevelInfo,
    AddSource: true,  // include file:line
}))

slog.SetDefault(logger)

// Structured logging with key-value pairs
slog.Info("User created",
    "userId", user.ID,
    "email", user.Email,
    "duration", time.Since(start),
)

slog.Error("Payment failed",
    "userId", user.ID,
    "amount", amount,
    "error", err,
)

// Child logger with common fields
reqLogger := logger.With(
    "requestId", requestID,
    "userId", userID,
)
reqLogger.Info("Processing request", "method", r.Method, "path", r.URL.Path)
```

---

## Best Practices

- Accept interfaces, return concrete types — maximizes flexibility for callers
- Always pass context.Context as the first parameter to any function doing I/O
- Always call cancel() from WithTimeout/WithCancel — use defer cancel()
- Use errors.Is() and errors.As() — never compare errors with ==
- Keep goroutines owned — always have a way to stop them
- Use sync.WaitGroup to wait for goroutines to finish
- Use buffered channels to prevent goroutine leaks
- Check for goroutine leaks with goleak in tests
- Prefer table-driven tests — they are idiomatic and scale well

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Goroutine leak | Goroutine blocked forever on channel | Always use context cancellation or done channel |
| Ignoring errors | Silent failures throughout program | Handle every error, even fmt.Println errors |
| Closure capture in goroutine | All goroutines share same loop variable | Pass variable as argument to goroutine function |
| Race condition | Concurrent map writes panic | Use sync.Mutex or sync.Map for shared state |
| nil interface confusion | (*T)(nil) does not equal nil interface | Return typed nils carefully, check interface nil |
| Blocking in goroutine | Goroutine never finishes | Use context deadline or timeout |
| No defer cancel | Context leak, resources not freed | Always defer cancel() immediately after WithTimeout |
| Error string starts with capital | Breaks go vet, style violation | Error strings should be lowercase, no punctuation |

---

## Related Skills

- **docker-expert**: For containerizing Go services
- **grpc-expert**: For Go gRPC services
- **kubernetes-expert**: For deploying Go apps to K8s
- **cli-tooling-expert**: For Go CLIs with Cobra
- **postgresql-expert**: For Go database patterns with pgx
- **testing-expert**: For Go testing strategy
