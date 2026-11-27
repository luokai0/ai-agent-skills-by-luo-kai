---
author: luo-kai
name: ios-expert
description: Expert-level iOS development with SwiftUI and UIKit. Use when building iOS apps, working with SwiftUI views, UIKit, Auto Layout, Core Data, networking, push notifications, App Store submission, or Xcode debugging. Also use when the user mentions 'SwiftUI', 'UIKit', '@State', 'Core Data', 'App Store Connect', 'Xcode', 'TestFlight', 'Swift', 'iOS build error', or 'simulator'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# iOS Development Expert

You are an expert iOS developer with deep knowledge of SwiftUI, UIKit, Swift concurrency, Core Data, and the Apple developer ecosystem.

## Before Starting

1. **UI framework** — SwiftUI, UIKit, or both?
2. **iOS target** — iOS 16, 17, 18? (affects available APIs)
3. **Architecture** — MVVM, TCA, MV, clean architecture?
4. **Problem type** — building feature, debugging, performance, App Store?
5. **Data persistence** — Core Data, SwiftData, UserDefaults, Keychain?

---

## Core Expertise Areas

- **SwiftUI**: views, modifiers, state management (@State, @Binding, @ObservableObject, @Observable)
- **Swift concurrency**: async/await, actors, Task, structured concurrency, MainActor
- **UIKit**: view lifecycle, Auto Layout, UITableView, UICollectionView, navigation
- **Data persistence**: Core Data, SwiftData (iOS 17+), UserDefaults, Keychain
- **Networking**: URLSession, async/await, Codable, error handling
- **Architecture**: MVVM with Combine/async-await, TCA basics
- **Performance**: Instruments, memory leaks, render performance
- **App Store**: signing, capabilities, App Store Connect, TestFlight, review guidelines

---

## Key Patterns & Code

### SwiftUI App Entry Point
```swift
import SwiftUI

@main
struct MyApp: App {
    @StateObject private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
                .onAppear {
                    setupAppearance()
                }
        }
    }

    private func setupAppearance() {
        UINavigationBar.appearance().largeTitleTextAttributes = [
            .foregroundColor: UIColor.label
        ]
    }
}
```

### State Management
```swift
// @State — local view state
struct CounterView: View {
    @State private var count = 0
    @State private var isShowingAlert = false

    var body: some View {
        VStack(spacing: 20) {
            Text('Count: \(count)')
                .font(.largeTitle)
            Button('Increment') {
                count += 1
                if count >= 10 { isShowingAlert = true }
            }
            .buttonStyle(.borderedProminent)
        }
        .alert('Reached 10!', isPresented: $isShowingAlert) {
            Button('Reset') { count = 0 }
            Button('Continue', role: .cancel) {}
        }
    }
}

// @Observable (iOS 17+) — modern replacement for ObservableObject
import Observation

@Observable
class UserStore {
    var users: [User] = []
    var isLoading = false
    var errorMessage: String?

    func fetchUsers() async {
        isLoading = true
        errorMessage = nil
        do {
            users = try await UserService.fetchAll()
        } catch {
            errorMessage = error.localizedDescription
        }
        isLoading = false
    }
}

// Use in view
struct UsersView: View {
    @State private var store = UserStore()

    var body: some View {
        Group {
            if store.isLoading {
                ProgressView()
            } else if let error = store.errorMessage {
                ContentUnavailableView(error, systemImage: 'exclamationmark.triangle')
            } else {
                List(store.users) { user in
                    UserRow(user: user)
                }
            }
        }
        .task { await store.fetchUsers() }
        .refreshable { await store.fetchUsers() }
    }
}

// @ObservableObject (iOS 13+) — pre-iOS 17 approach
class CartViewModel: ObservableObject {
    @Published var items: [CartItem] = []
    @Published var isCheckingOut = false

    var total: Double {
        items.reduce(0) { $0 + $1.price * Double($1.quantity) }
    }

    func addItem(_ item: CartItem) {
        if let index = items.firstIndex(where: { $0.id == item.id }) {
            items[index].quantity += 1
        } else {
            items.append(item)
        }
    }

    func removeItem(_ item: CartItem) {
        items.removeAll { $0.id == item.id }
    }
}
```

### Navigation
```swift
// NavigationStack (iOS 16+) — programmatic navigation with type-safe paths
struct AppView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            HomeView(path: $path)
                .navigationDestination(for: User.self) { user in
                    UserDetailView(user: user)
                }
                .navigationDestination(for: Product.self) { product in
                    ProductDetailView(product: product)
                }
        }
    }
}

struct HomeView: View {
    @Binding var path: NavigationPath
    let users: [User] = []

    var body: some View {
        List(users) { user in
            Button(user.name) {
                path.append(user)  // type-safe navigation
            }
        }
        .navigationTitle('Home')
        .toolbar {
            Button('Settings') {
                path.append(SettingsRoute.main)
            }
        }
    }
}

// Sheet and fullScreenCover presentation
struct ContentView: View {
    @State private var selectedUser: User?
    @State private var isShowingSettings = false

    var body: some View {
        Text('Content')
            .sheet(item: $selectedUser) { user in
                UserDetailSheet(user: user)
                    .presentationDetents([.medium, .large])
                    .presentationDragIndicator(.visible)
            }
            .fullScreenCover(isPresented: $isShowingSettings) {
                SettingsView()
            }
    }
}
```

### Async/Await Networking
```swift
import Foundation

enum NetworkError: LocalizedError {
    case invalidURL
    case invalidResponse(statusCode: Int)
    case decodingError(Error)
    case unauthorized

    var errorDescription: String? {
        switch self {
        case .invalidURL:              return 'Invalid URL'
        case .invalidResponse(let code): return 'Server error \(code)'
        case .decodingError(let error): return 'Decoding error: \(error)'
        case .unauthorized:            return 'Please log in again'
        }
    }
}

actor APIClient {
    private let session: URLSession
    private let baseURL: URL
    private var authToken: String?

    init(baseURL: URL) {
        self.baseURL = baseURL
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 30
        self.session = URLSession(configuration: config)
    }

    func setToken(_ token: String) {
        self.authToken = token
    }

    func fetch<T: Decodable>(
        _ endpoint: String,
        method: String = 'GET',
        body: Encodable? = nil
    ) async throws -> T {
        guard let url = URL(string: endpoint, relativeTo: baseURL) else {
            throw NetworkError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue('application/json', forHTTPHeaderField: 'Content-Type')

        if let token = authToken {
            request.setValue('Bearer \(token)', forHTTPHeaderField: 'Authorization')
        }

        if let body = body {
            request.httpBody = try JSONEncoder().encode(body)
        }

        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse(statusCode: 0)
        }

        switch httpResponse.statusCode {
        case 200...299: break
        case 401: throw NetworkError.unauthorized
        default: throw NetworkError.invalidResponse(statusCode: httpResponse.statusCode)
        }

        do {
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            decoder.dateDecodingStrategy = .iso8601
            return try decoder.decode(T.self, from: data)
        } catch {
            throw NetworkError.decodingError(error)
        }
    }
}

// Usage
let client = APIClient(baseURL: URL(string: 'https://api.example.com')!)

do {
    let users: [User] = try await client.fetch('/users')
    print('Fetched \(users.count) users')
} catch {
    print('Error:', error.localizedDescription)
}
```

### SwiftData (iOS 17+)
```swift
import SwiftData
import SwiftUI

@Model
final class Task {
    var id: UUID
    var title: String
    var isCompleted: Bool
    var createdAt: Date
    var priority: Int

    init(title: String, priority: Int = 1) {
        self.id = UUID()
        self.title = title
        self.isCompleted = false
        self.createdAt = Date()
        self.priority = priority
    }
}

// App setup
@main
struct TaskApp: App {
    var body: some Scene {
        WindowGroup {
            TaskListView()
        }
        .modelContainer(for: Task.self)
    }
}

// View with SwiftData
struct TaskListView: View {
    @Environment(\.modelContext) private var context
    @Query(sort: \Task.createdAt, order: .reverse) private var tasks: [Task]
    @State private var newTaskTitle = ''

    // Filtered query
    @Query(filter: #Predicate<Task> { !$0.isCompleted },
           sort: \Task.priority, order: .reverse)
    private var pendingTasks: [Task]

    var body: some View {
        List {
            ForEach(tasks) { task in
                TaskRow(task: task)
            }
            .onDelete { indexSet in
                for index in indexSet {
                    context.delete(tasks[index])
                }
            }
        }
        .navigationTitle('Tasks (\(tasks.count))')
        .toolbar {
            Button('Add') {
                let task = Task(title: 'New Task')
                context.insert(task)
            }
        }
    }
}

struct TaskRow: View {
    let task: Task

    var body: some View {
        HStack {
            Image(systemName: task.isCompleted ? 'checkmark.circle.fill' : 'circle')
                .foregroundStyle(task.isCompleted ? .green : .secondary)
                .onTapGesture { task.isCompleted.toggle() }
            Text(task.title)
                .strikethrough(task.isCompleted)
        }
    }
}
```

### Custom ViewModifier and Extension
```swift
// Reusable card modifier
struct CardModifier: ViewModifier {
    var radius: CGFloat = 12
    var shadow: Bool = true

    func body(content: Content) -> some View {
        content
            .background(.background)
            .clipShape(RoundedRectangle(cornerRadius: radius))
            .if(shadow) { view in
                view.shadow(color: .black.opacity(0.1), radius: 8, x: 0, y: 2)
            }
    }
}

extension View {
    func card(radius: CGFloat = 12, shadow: Bool = true) -> some View {
        modifier(CardModifier(radius: radius, shadow: shadow))
    }

    // Conditional modifier
    @ViewBuilder
    func `if`<Transform: View>(_ condition: Bool, transform: (Self) -> Transform) -> some View {
        if condition {
            transform(self)
        } else {
            self
        }
    }

    // Loading overlay
    func loading(_ isLoading: Bool) -> some View {
        overlay {
            if isLoading {
                ZStack {
                    Color.black.opacity(0.3)
                    ProgressView()
                        .progressViewStyle(.circular)
                        .tint(.white)
                }
                .ignoresSafeArea()
            }
        }
    }
}

// Usage
VStack { /* content */ }
    .padding()
    .card(radius: 16)
    .loading(viewModel.isLoading)
```

### Keychain Storage
```swift
import Security
import Foundation

enum KeychainError: Error {
    case itemNotFound
    case duplicateItem
    case unexpectedStatus(OSStatus)
}

struct Keychain {
    static func save(key: String, data: Data) throws {
        let query: [String: Any] = [
            kSecClass as String:       kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String:   data,
        ]
        SecItemDelete(query as CFDictionary)  // delete existing first
        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess else {
            throw KeychainError.unexpectedStatus(status)
        }
    }

    static func load(key: String) throws -> Data {
        let query: [String: Any] = [
            kSecClass as String:       kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String:  kCFBooleanTrue!,
            kSecMatchLimit as String:  kSecMatchLimitOne,
        ]
        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)
        guard status == errSecSuccess, let data = result as? Data else {
            throw KeychainError.itemNotFound
        }
        return data
    }

    static func delete(key: String) {
        let query: [String: Any] = [
            kSecClass as String:       kSecClassGenericPassword,
            kSecAttrAccount as String: key,
        ]
        SecItemDelete(query as CFDictionary)
    }
}

// @propertyWrapper for easy Keychain access
@propertyWrapper
struct KeychainStorage {
    let key: String

    var wrappedValue: String? {
        get {
            try? String(data: Keychain.load(key: key), encoding: .utf8)
        }
        set {
            if let value = newValue {
                try? Keychain.save(key: key, data: Data(value.utf8))
            } else {
                Keychain.delete(key: key)
            }
        }
    }
}

// Usage
@KeychainStorage(key: 'auth_token')
var authToken: String?
```

---

## Best Practices

- Use SwiftUI for new iOS 16+ projects — UIKit for complex custom UI or legacy
- Use @Observable (iOS 17+) over @ObservableObject — simpler, more performant
- Use Swift concurrency (async/await) over Combine for networking
- Always use MainActor for UI updates from async code
- Store sensitive data in Keychain — never UserDefaults
- Use .task modifier instead of onAppear for async work — it handles cancellation
- Test on real devices — simulators do not reflect real performance
- Use Instruments Time Profiler and Leaks before submitting to App Store

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| @State in wrong place | State resets unexpectedly | Put shared state in parent or @Observable class |
| UI updates off MainActor | Purple runtime warning, crashes | Annotate with @MainActor |
| Retain cycles in closures | Memory leaks | Use [weak self] in escaping closures |
| Sensitive data in UserDefaults | Readable by anyone with device access | Use Keychain for tokens and credentials |
| Missing .task cancellation | Network request continues after view disappears | Use .task modifier which auto-cancels |
| Overusing @EnvironmentObject | Hard to debug, crashes if not provided | Use sparingly, document requirements |
| Large views | Slow SwiftUI diffing | Break into smaller focused views |
| Force unwrapping | Runtime crashes | Use guard let, if let, or nil coalescing |

---

## Related Skills

- **swift-expert**: For Swift language deep dive
- **react-native-expert**: For cross-platform mobile development
- **android-expert**: For Android counterpart patterns
- **appsec-expert**: For iOS security best practices
- **cicd-expert**: For Xcode Cloud and Fastlane CI/CD
- **testing-expert**: For XCTest and UI testing