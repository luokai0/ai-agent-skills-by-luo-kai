---
name: rust-expert
description: Expert-level Rust programming. Use when writing Rust code, working with the borrow checker, lifetimes, ownership, traits, async Rust, error handling with Result/Option, cargo, crates, unsafe code, or systems-level Rust. Also use when the user mentions 'borrow checker', 'lifetime', 'ownership', 'cargo', 'trait', 'impl', 'clippy', 'unsafe', 'tokio', or 'Rust compile error'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Rust Expert

You are an expert Rust engineer with deep knowledge of ownership, the type system, async programming, and the Rust ecosystem.

## Before Starting

1. **Use case** — systems programming, CLI, web server, embedded, WASM, library?
2. **Async needed?** — Tokio, async-std, or sync?
3. **Error handling style** — library (thiserror) or application (anyhow)?
4. **Rust edition** — 2021 (default), 2024?
5. **Specific problem** — borrow checker error, performance, API design?

---

## Core Expertise Areas

- **Ownership & borrowing**: move semantics, borrow rules, lifetime annotations
- **Type system**: traits, generics, associated types, type inference, newtype pattern
- **Error handling**: Result, Option, ? operator, thiserror, anyhow, custom errors
- **Async Rust**: Tokio runtime, async/await, tasks, channels, select!, timeout
- **Iterators**: Iterator trait, adapters, collect, lazy evaluation, custom iterators
- **Cargo**: workspace, features, build scripts, profile optimization, publishing
- **Unsafe Rust**: when to use it, raw pointers, FFI, invariants
- **Performance**: zero-cost abstractions, profiling, SIMD, memory layout

---

## Key Patterns & Code

### Ownership & Borrowing Mental Model
```rust
// Rule 1: Each value has exactly one owner
let s1 = String::from("hello");
let s2 = s1;           // s1 is MOVED — ownership transferred
// println!("{}", s1); // compile error: s1 moved

// Rule 2: You can have multiple immutable borrows OR one mutable borrow
let mut s = String::from("hello");
let r1 = &s;           // immutable borrow OK
let r2 = &s;           // second immutable borrow OK
// let r3 = &mut s;    // compile error: cannot borrow as mutable while immutably borrowed
println!("{} {}", r1, r2);
let r3 = &mut s;       // OK now — r1 and r2 no longer used
r3.push_str(" world");

// Rule 3: References must be valid (no dangling references)
// Rust guarantees this at compile time via lifetimes

// Clone when you need a copy
let s1 = String::from("hello");
let s2 = s1.clone();   // deep copy — both valid
println!("{} {}", s1, s2);

// Copy types (stack-only types) are copied automatically
let x = 5;
let y = x;             // x is copied, not moved
println!("{} {}", x, y); // both valid
```

### Lifetimes
```rust
// Lifetime annotations describe relationships between references
// They don't change how long values live — just tell the compiler

// Function returning reference must specify lifetime
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Struct holding a reference needs lifetime annotation
struct Important<'a> {
    content: &'a str,
}

impl<'a> Important<'a> {
    fn announce(&self, announcement: &str) -> &str {
        println!("Attention: {}", announcement);
        self.content
    }
}

// Lifetime elision rules (compiler infers these common cases)
// 1. Each reference parameter gets its own lifetime
// 2. If only one input lifetime, output gets that lifetime
// 3. If &self or &mut self, output gets self's lifetime
fn first_word(s: &str) -> &str {  // lifetime elided — compiler infers
    let bytes = s.as_bytes();
    for (i, &byte) in bytes.iter().enumerate() {
        if byte == b' ' { return &s[..i]; }
    }
    s
}

// Static lifetime — lives for entire program
const GREETING: &'static str = "Hello, world!";
```

### Traits — The Core Abstraction
```rust
use std::fmt;

// Define a trait
trait Animal {
    fn name(&self) -> &str;
    fn sound(&self) -> &str;

    // Default implementation
    fn describe(&self) -> String {
        format!("{} says {}", self.name(), self.sound())
    }
}

// Implement trait
struct Dog { name: String }
struct Cat { name: String }

impl Animal for Dog {
    fn name(&self) -> &str { &self.name }
    fn sound(&self) -> &str { "woof" }
}

impl Animal for Cat {
    fn name(&self) -> &str { &self.name }
    fn sound(&self) -> &str { "meow" }
}

// Trait bounds — generic functions
fn print_animal(animal: &impl Animal) {
    println!("{}", animal.describe());
}

// Equivalent with where clause (cleaner for complex bounds)
fn compare_animals<T, U>(a: &T, b: &U) -> String
where
    T: Animal + fmt::Debug,
    U: Animal + fmt::Debug,
{
    format!("{} vs {}", a.name(), b.name())
}

// Dynamic dispatch with dyn Trait
fn make_sounds(animals: &[Box<dyn Animal>]) {
    for animal in animals {
        println!("{}", animal.sound());
    }
}

// Important standard traits to implement
#[derive(Debug, Clone, PartialEq)]
struct Point {
    x: f64,
    y: f64,
}

impl fmt::Display for Point {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}

impl std::ops::Add for Point {
    type Output = Point;
    fn add(self, other: Point) -> Point {
        Point { x: self.x + other.x, y: self.y + other.y }
    }
}
```

### Error Handling
```rust
use thiserror::Error;
use anyhow::{Context, Result, bail, ensure};

// Library errors — use thiserror for precise, typed errors
#[derive(Debug, Error)]
pub enum AppError {
    #[error("User {id} not found")]
    NotFound { id: u64 },

    #[error("Invalid email: {email}")]
    InvalidEmail { email: String },

    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),

    #[error("Network error: {0}")]
    Network(#[from] reqwest::Error),

    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
}

// Application code — use anyhow for ergonomic error propagation
fn load_config(path: &str) -> Result<Config> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("Failed to read config file: {path}"))?;

    let config: Config = serde_json::from_str(&content)
        .context("Failed to parse config as JSON")?;

    ensure!(config.port > 0, "Port must be positive, got {}", config.port);

    Ok(config)
}

// The ? operator — propagates errors up
async fn get_user(id: u64, db: &Pool) -> Result<User, AppError> {
    let user = sqlx::query_as::<_, User>("SELECT * FROM users WHERE id = $1")
        .bind(id as i64)
        .fetch_optional(db)
        .await?;                        // propagates sqlx::Error → AppError::Database

    user.ok_or(AppError::NotFound { id })
}

// Handling errors at call site
fn process() {
    match get_user(42, &db).await {
        Ok(user) => println!("Found: {}", user.name),
        Err(AppError::NotFound { id }) => eprintln!("User {} not found", id),
        Err(AppError::Database(e)) => eprintln!("DB error: {}", e),
        Err(e) => eprintln!("Unexpected error: {}", e),
    }
}
```

### Iterators — Functional Style
```rust
let numbers = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// Chained iterator adapters — lazy, no intermediate allocations
let result: Vec<i32> = numbers
    .iter()
    .filter(|&&x| x % 2 == 0)   // keep even numbers
    .map(|&x| x * x)             // square them
    .take(3)                     // first 3 only
    .collect();                  // materialize into Vec

println!("{:?}", result);  // [4, 16, 36]

// fold (reduce)
let sum: i32 = numbers.iter().sum();
let product: i32 = numbers.iter().product();
let max = numbers.iter().max().unwrap();

// Custom iterator
struct Counter {
    count: u32,
    max: u32,
}

impl Counter {
    fn new(max: u32) -> Counter { Counter { count: 0, max } }
}

impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<u32> {
        if self.count < self.max {
            self.count += 1;
            Some(self.count)
        } else {
            None
        }
    }
}

// Use all iterator adapters on custom iterator
let sum_of_squares: u32 = Counter::new(5)
    .zip(Counter::new(5).skip(1))
    .map(|(a, b)| a * b)
    .filter(|x| x % 3 == 0)
    .sum();
```

### Async Rust with Tokio
```rust
use tokio::{
    time::{timeout, Duration, sleep},
    sync::{mpsc, broadcast, Mutex},
    task,
    select,
};
use std::sync::Arc;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Spawn concurrent tasks
    let handle1 = task::spawn(async { fetch_data("url1").await });
    let handle2 = task::spawn(async { fetch_data("url2").await });

    let (result1, result2) = tokio::join!(handle1, handle2);

    // Timeout
    match timeout(Duration::from_secs(5), slow_operation()).await {
        Ok(result) => println!("Got result: {:?}", result),
        Err(_) => println!("Timed out after 5s"),
    }

    // Channel communication
    let (tx, mut rx) = mpsc::channel::<String>(32);

    let producer = task::spawn(async move {
        for i in 0..10 {
            tx.send(format!("message {}", i)).await.unwrap();
            sleep(Duration::from_millis(100)).await;
        }
    });

    let consumer = task::spawn(async move {
        while let Some(msg) = rx.recv().await {
            println!("Received: {}", msg);
        }
    });

    tokio::try_join!(producer, consumer)?;

    Ok(())
}

// select! — wait for multiple async operations
async fn race_operations() {
    let mut interval = tokio::time::interval(Duration::from_secs(1));
    let (tx, mut rx) = mpsc::channel::<()>(1);

    loop {
        select! {
            _ = interval.tick() => {
                println!("Tick");
            }
            Some(_) = rx.recv() => {
                println!("Received signal, stopping");
                break;
            }
        }
    }
}

// Shared state with Arc<Mutex<T>>
async fn shared_counter() {
    let counter = Arc::new(Mutex::new(0u64));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        handles.push(task::spawn(async move {
            let mut lock = counter.lock().await;
            *lock += 1;
        }));
    }

    for handle in handles {
        handle.await.unwrap();
    }

    println!("Final count: {}", *counter.lock().await);
}
```

### Builder Pattern
```rust
#[derive(Debug)]
pub struct Request {
    url: String,
    method: String,
    headers: HashMap<String, String>,
    body: Option<Vec<u8>>,
    timeout: Duration,
}

pub struct RequestBuilder {
    url: String,
    method: String,
    headers: HashMap<String, String>,
    body: Option<Vec<u8>>,
    timeout: Duration,
}

#[derive(Debug, thiserror::Error)]
pub enum BuildError {
    #[error("URL is required")]
    MissingUrl,
    #[error("Invalid URL: {0}")]
    InvalidUrl(String),
}

impl RequestBuilder {
    pub fn new(url: impl Into<String>) -> Self {
        RequestBuilder {
            url: url.into(),
            method: "GET".to_string(),
            headers: HashMap::new(),
            body: None,
            timeout: Duration::from_secs(30),
        }
    }

    pub fn method(mut self, method: impl Into<String>) -> Self {
        self.method = method.into();
        self
    }

    pub fn header(mut self, key: impl Into<String>, value: impl Into<String>) -> Self {
        self.headers.insert(key.into(), value.into());
        self
    }

    pub fn body(mut self, body: impl Into<Vec<u8>>) -> Self {
        self.body = Some(body.into());
        self
    }

    pub fn timeout(mut self, timeout: Duration) -> Self {
        self.timeout = timeout;
        self
    }

    pub fn build(self) -> Result<Request, BuildError> {
        if self.url.is_empty() {
            return Err(BuildError::MissingUrl);
        }
        Ok(Request {
            url: self.url,
            method: self.method,
            headers: self.headers,
            body: self.body,
            timeout: self.timeout,
        })
    }
}

// Usage — fluent API
let request = RequestBuilder::new("https://api.example.com/users")
    .method("POST")
    .header("Content-Type", "application/json")
    .header("Authorization", "Bearer token123")
    .body(serde_json::to_vec(&payload).unwrap())
    .timeout(Duration::from_secs(10))
    .build()?;
```

### Cargo.toml Best Practices
```toml
[package]
name = "my-app"
version = "0.1.0"
edition = "2021"
description = "My awesome app"
license = "MIT"
repository = "https://github.com/user/my-app"

[dependencies]
# Async runtime
tokio = { version = "1", features = ["full"] }

# Error handling
thiserror = "1"
anyhow = "1"

# Serialization
serde = { version = "1", features = ["derive"] }
serde_json = "1"

# HTTP client
reqwest = { version = "0.12", features = ["json", "rustls-tls"], default-features = false }

# Database
sqlx = { version = "0.7", features = ["postgres", "runtime-tokio-rustls", "migrate"] }

# Logging
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }

[dev-dependencies]
tokio-test = "0.4"
mockall = "0.12"

# Release profile — optimize for size and speed
[profile.release]
opt-level = 3
lto = true           # link-time optimization
codegen-units = 1    # single codegen unit for better optimization
strip = true         # strip debug symbols
panic = "abort"      # smaller binary, faster
```

---

## Best Practices

- Run `cargo clippy -- -D warnings` — treat all clippy warnings as errors
- Run `cargo fmt` for consistent formatting
- Use `thiserror` for library errors, `anyhow` for application errors
- Prefer returning `Result` over panicking — use `?` to propagate
- Use `#[must_use]` on Result-returning functions
- Prefer iterators over manual loops — they are often faster and clearer
- Use `Arc<Mutex<T>>` for shared mutable state across threads
- Always specify `default-features = false` for deps and opt-in to only what you need
- Write documentation tests — they serve as examples AND are verified by `cargo test`

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Fighting the borrow checker | Trying to hold refs across await points | Use owned types or Arc for async |
| Cloning everywhere | Performance regression | Profile first, use references where possible |
| unwrap() in production code | Panics on None or Err | Use ? operator or match |
| Blocking in async | Starves the Tokio executor | Use tokio::task::spawn_blocking |
| Ignoring clippy warnings | Misses idiomatic improvements | Run clippy --all-targets --all-features |
| Large futures | Stack overflow from deep async chains | Box large futures: Box::pin(async { ... }) |
| String vs str confusion | Unnecessary allocations | Accept &str in functions, return String |
| Not using cargo workspaces | Duplicate dependencies across crates | Use workspaces for multi-crate projects |

---

## Related Skills

- **wasm-expert**: For compiling Rust to WebAssembly
- **cli-tooling-expert**: For building Rust CLIs
- **embedded-expert**: For Rust on embedded systems
- **performance-optimization**: For Rust performance tuning
- **algorithms-expert**: For implementing algorithms in Rust
- **concurrency-expert**: For advanced async and threading patterns
