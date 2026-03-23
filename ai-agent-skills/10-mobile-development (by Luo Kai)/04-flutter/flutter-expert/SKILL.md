---
author: luo-kai
name: flutter-expert
description: Expert-level Flutter development. Use when building Flutter apps, working with widgets, state management (Riverpod, BLoC, Provider), platform channels, animations, or deploying Flutter apps to iOS and Android. Also use when the user mentions 'Flutter', 'Widget', 'Riverpod', 'BLoC', 'Dart', 'go_router', 'flutter pub', 'pubspec.yaml', 'hot reload', or 'platform channel'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Flutter Expert

You are an expert Flutter developer with deep knowledge of Dart, widget composition, state management with Riverpod, animations, platform channels, and shipping Flutter apps.

## Before Starting

1. **Flutter version** — stable channel? Flutter 3.16, 3.19, 3.22?
2. **State management** — Riverpod, BLoC, Provider, GetX, or plain setState?
3. **Navigation** — go_router, Navigator 2.0, or AutoRoute?
4. **Target platforms** — iOS and Android only, or web and desktop too?
5. **Problem type** — building UI, state management, platform integration, performance?

---

## Core Expertise Areas

- **Widget system**: StatelessWidget, StatefulWidget, InheritedWidget, keys
- **Riverpod 2.0**: Provider, StateNotifier, AsyncNotifier, family, autoDispose
- **BLoC pattern**: events, states, transitions, bloc_test
- **go_router**: declarative routing, deep linking, nested navigation, guards
- **Animations**: AnimationController, Tween, implicit animations, Hero
- **Platform channels**: MethodChannel, EventChannel, FFI
- **Performance**: const widgets, RepaintBoundary, ListView.builder, profiling
- **Testing**: widget tests, unit tests, integration tests, golden tests

---

## Key Patterns & Code

### App Setup with Riverpod and go_router
```dart
// main.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const ProviderScope(child: MyApp()));
}

class MyApp extends ConsumerWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(routerProvider);
    return MaterialApp.router(
      title: 'My App',
      theme: AppTheme.light,
      darkTheme: AppTheme.dark,
      themeMode: ThemeMode.system,
      routerConfig: router,
      debugShowCheckedModeBanner: false,
    );
  }
}

// router.dart
final routerProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authStateProvider);

  return GoRouter(
    initialLocation: '/',
    redirect: (context, state) {
      final isAuthenticated = authState.isAuthenticated;
      final isOnAuth = state.matchedLocation.startsWith('/auth');
      if (!isAuthenticated && !isOnAuth) return '/auth/login';
      if (isAuthenticated && isOnAuth) return '/';
      return null;
    },
    routes: [
      GoRoute(path: '/', builder: (context, state) => const HomeScreen()),
      GoRoute(
        path: '/users/:id',
        builder: (context, state) {
          final id = state.pathParameters['id']!;
          return UserDetailScreen(userId: id);
        },
      ),
      ShellRoute(
        builder: (context, state, child) => AppShell(child: child),
        routes: [
          GoRoute(path: '/home', builder: (_, __) => const HomeTab()),
          GoRoute(path: '/profile', builder: (_, __) => const ProfileTab()),
          GoRoute(path: '/settings', builder: (_, __) => const SettingsTab()),
        ],
      ),
      GoRoute(path: '/auth/login', builder: (context, state) => const LoginScreen()),
    ],
  );
});
```

### Riverpod 2.0 — State Management
```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'users_provider.g.dart';

// AsyncNotifier with code generation
@riverpod
class Users extends _$Users {
  @override
  Future<List<User>> build() async {
    return ref.read(userRepositoryProvider).getUsers();
  }

  Future<void> refresh() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(
      () => ref.read(userRepositoryProvider).getUsers()
    );
  }

  Future<void> deleteUser(String userId) async {
    await ref.read(userRepositoryProvider).deleteUser(userId);
    ref.invalidateSelf();
  }
}

// Family provider — parameterized by userId
@riverpod
Future<User> userById(UserByIdRef ref, String userId) async {
  return ref.read(userRepositoryProvider).getUserById(userId);
}

// StateNotifier — synchronous complex state
@riverpod
class CartNotifier extends _$CartNotifier {
  @override
  List<CartItem> build() => [];

  void addItem(Product product) {
    final existing = state.indexWhere((i) => i.productId == product.id);
    if (existing != -1) {
      state = [
        for (int i = 0; i < state.length; i++)
          if (i == existing)
            state[i].copyWith(quantity: state[i].quantity + 1)
          else
            state[i],
      ];
    } else {
      state = [...state, CartItem(productId: product.id, quantity: 1)];
    }
  }

  void removeItem(String productId) {
    state = state.where((i) => i.productId != productId).toList();
  }

  void clear() => state = [];
}

// Using in widget
class UsersScreen extends ConsumerWidget {
  const UsersScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final usersAsync = ref.watch(usersProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Users')),
      body: usersAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => ErrorWidget(error.toString()),
        data: (users) => ListView.builder(
          itemCount: users.length,
          itemBuilder: (context, index) => UserTile(user: users[index]),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => ref.read(usersProvider.notifier).refresh(),
        child: const Icon(Icons.refresh),
      ),
    );
  }
}
```

### Widget Composition
```dart
class AppCard extends StatelessWidget {
  const AppCard({
    super.key,
    required this.child,
    this.onTap,
    this.padding,
  });

  final Widget child;
  final VoidCallback? onTap;
  final EdgeInsetsGeometry? padding;

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.08),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(12),
          child: Padding(
            padding: padding ?? const EdgeInsets.all(16),
            child: child,
          ),
        ),
      ),
    );
  }
}
```

### Animations
```dart
// Implicit animation
class AnimatedCard extends StatefulWidget {
  const AnimatedCard({super.key, required this.isSelected});
  final bool isSelected;

  @override
  State<AnimatedCard> createState() => _AnimatedCardState();
}

class _AnimatedCardState extends State<AnimatedCard> {
  @override
  Widget build(BuildContext context) {
    return AnimatedContainer(
      duration: const Duration(milliseconds: 200),
      curve: Curves.easeInOut,
      decoration: BoxDecoration(
        color: widget.isSelected ? Colors.blue : Colors.white,
        borderRadius: BorderRadius.circular(widget.isSelected ? 16 : 8),
      ),
      child: AnimatedDefaultTextStyle(
        duration: const Duration(milliseconds: 200),
        style: TextStyle(
          color: widget.isSelected ? Colors.white : Colors.black,
          fontWeight: widget.isSelected ? FontWeight.bold : FontWeight.normal,
        ),
        child: const Text('Card'),
      ),
    );
  }
}

// Explicit animation with AnimationController
class PulseAnimation extends StatefulWidget {
  const PulseAnimation({super.key, required this.child});
  final Widget child;

  @override
  State<PulseAnimation> createState() => _PulseAnimationState();
}

class _PulseAnimationState extends State<PulseAnimation>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late final Animation<double> _scale;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1000),
    )..repeat(reverse: true);

    _scale = Tween<double>(begin: 1.0, end: 1.1).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ScaleTransition(scale: _scale, child: widget.child);
  }
}
```

### Platform Channels
```dart
import 'package:flutter/services.dart';

class BiometricsService {
  static const _channel = MethodChannel('com.example.app/biometrics');

  Future<bool> isAvailable() async {
    try {
      return await _channel.invokeMethod<bool>('isAvailable') ?? false;
    } on PlatformException catch (e) {
      debugPrint('Biometrics error: \${e.message}');
      return false;
    }
  }

  Future<bool> authenticate(String reason) async {
    try {
      return await _channel.invokeMethod<bool>('authenticate', {
        'reason': reason,
      }) ?? false;
    } on PlatformException catch (e) {
      debugPrint('Auth error: \${e.code} - \${e.message}');
      return false;
    }
  }
}

// Event channel for continuous streams
class LocationService {
  static const _channel = EventChannel('com.example.app/location');

  Stream<Map<String, double>> get locationStream {
    return _channel.receiveBroadcastStream().map((event) {
      final map = event as Map<dynamic, dynamic>;
      return {
        'lat': map['lat'] as double,
        'lng': map['lng'] as double,
      };
    });
  }
}
```

### Performance — const and Keys
```dart
// Use const wherever possible
class ProductList extends StatelessWidget {
  const ProductList({super.key, required this.products});
  final List<Product> products;

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: products.length,
      itemBuilder: (context, index) {
        final product = products[index];
        return ProductTile(
          key: ValueKey(product.id),
          product: product,
        );
      },
    );
  }
}

// RepaintBoundary — isolate expensive repaints
RepaintBoundary(
  child: HeavyAnimationWidget(),
)

// const throughout
class EmptyState extends StatelessWidget {
  const EmptyState({super.key});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.inbox, size: 64, color: Colors.grey),
          SizedBox(height: 16),
          Text('No items found', style: TextStyle(color: Colors.grey)),
        ],
      ),
    );
  }
}
```

### pubspec.yaml
```yaml
name: my_app
description: My Flutter app
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'
  flutter: '>=3.16.0'

dependencies:
  flutter:
    sdk: flutter
  flutter_riverpod: ^2.4.0
  riverpod_annotation: ^2.3.0
  go_router: ^13.0.0
  dio: ^5.4.0
  flutter_secure_storage: ^9.0.0
  shared_preferences: ^2.2.0
  cached_network_image: ^3.3.0
  freezed_annotation: ^2.4.0
  json_annotation: ^4.8.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  build_runner: ^2.4.0
  riverpod_generator: ^2.3.0
  freezed: ^2.4.0
  json_serializable: ^6.7.0
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
  assets:
    - assets/images/
  fonts:
    - family: Poppins
      fonts:
        - asset: assets/fonts/Poppins-Regular.ttf
        - asset: assets/fonts/Poppins-Bold.ttf
          weight: 700
```

---

## Best Practices

- Use const constructors everywhere possible — prevents unnecessary rebuilds
- Use ListView.builder (lazy) not ListView (eager) for any list with 10+ items
- Use keys when dynamically reordering or inserting list items
- Use RepaintBoundary around expensive or frequently-repainting widgets
- Use ConsumerWidget over Consumer widget for cleaner code
- Prefer autoDispose on providers that should not persist indefinitely
- Run flutter analyze and fix all warnings before committing
- Profile with DevTools before optimizing — guesswork is usually wrong

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| setState in StatelessWidget | Compile error | Use StatefulWidget or ConsumerWidget |
| No const constructors | Excessive rebuilds | Add const to widget constructors |
| ListView not ListView.builder | All items built at once | Always use ListView.builder |
| Missing dispose() | AnimationController leak | Always dispose controllers in dispose() |
| context across async gaps | Context might not be mounted | Check mounted before using context after await |
| No key on list items | Wrong animation and state on reorder | Always use ValueKey with stable ID |
| Heavy computation in build() | Jank on every rebuild | Move to provider or use compute() |
| Nested Scaffolds | Weird behavior, double back buttons | One Scaffold per route |

---

## Related Skills

- **react-native-expert**: For React Native cross-platform alternative
- **ios-expert**: For native iOS integration via platform channels
- **android-expert**: For native Android integration via platform channels
- **cicd-expert**: For Flutter CI/CD with Fastlane or GitHub Actions
- **appsec-expert**: For Flutter app security patterns
- **testing-expert**: For Flutter widget and integration testing
