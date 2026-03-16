---
name: react-native-expert
description: Expert-level React Native development. Use when building cross-platform mobile apps with React Native, working with navigation, native modules, Expo, animations (Reanimated), performance optimization, or publishing to app stores. Also use when the user mentions 'React Native', 'Expo', 'React Navigation', 'Reanimated', 'native module', 'iOS build', 'Android build', 'metro bundler', or 'app store publishing'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# React Native Expert

You are an expert React Native engineer with deep knowledge of cross-platform mobile development, performance optimization, native integrations, and app store deployment.

## Before Starting

1. **Workflow** — Expo managed, Expo bare, or plain React Native CLI?
2. **React Native version** — 0.72, 0.73, 0.74, 0.75?
3. **Navigation** — React Navigation v6, Expo Router?
4. **State management** — Zustand, Redux, Jotai, React Query?
5. **Problem type** — building feature, performance issue, native module, publishing?

---

## Core Expertise Areas

- **Expo workflow**: managed vs bare, config plugins, EAS Build, EAS Submit
- **Navigation**: React Navigation (stack, tab, drawer), Expo Router, deep linking
- **Animations**: Reanimated 3, Gesture Handler, Skia, Lottie
- **Performance**: JS thread vs UI thread, Hermes, FlashList, image optimization
- **Native modules**: Turbo Modules, JSI, bridgeless architecture (RN 0.73+)
- **Platform-specific**: Platform.OS, platform-specific files (.ios.tsx, .android.tsx)
- **Device APIs**: camera, location, push notifications, biometrics, storage
- **Publishing**: EAS Build, EAS Submit, app signing, TestFlight, Play Console

---

## Key Patterns & Code

### Project Setup — Expo (Recommended)
```bash
# Create new Expo project
npx create-expo-app MyApp --template blank-typescript
cd MyApp

# Essential dependencies
npx expo install expo-router expo-constants expo-linking
npx expo install react-native-reanimated react-native-gesture-handler
npx expo install @shopify/flash-list
npx expo install expo-image
npx expo install expo-secure-store
npx expo install expo-notifications

# Start development
npx expo start
npx expo start --ios      # iOS simulator
npx expo start --android  # Android emulator
```

### App Entry with Expo Router
```typescript
// app/_layout.tsx — root layout
import { Stack } from 'expo-router';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { StatusBar } from 'expo-status-bar';

const queryClient = new QueryClient();

export default function RootLayout() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <QueryClientProvider client={queryClient}>
        <StatusBar style='auto' />
        <Stack>
          <Stack.Screen name='(tabs)' options={{ headerShown: false }} />
          <Stack.Screen name='modal' options={{ presentation: 'modal' }} />
          <Stack.Screen
            name='product/[id]'
            options={{ title: 'Product Details' }}
          />
        </Stack>
      </QueryClientProvider>
    </GestureHandlerRootView>
  );
}

// app/(tabs)/_layout.tsx — bottom tab navigator
import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: '#007AFF',
        tabBarStyle: { paddingBottom: 5 },
      }}
    >
      <Tabs.Screen
        name='index'
        options={{
          title: 'Home',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name='home' size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name='profile'
        options={{
          title: 'Profile',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name='person' size={size} color={color} />
          ),
        }}
      />
    </Tabs>
  );
}

// app/product/[id].tsx — dynamic route
import { useLocalSearchParams, Stack } from 'expo-router';
import { View, Text } from 'react-native';

export default function ProductScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();

  return (
    <>
      <Stack.Screen options={{ title: 'Product ' + id }} />
      <View style={{ flex: 1, padding: 16 }}>
        <Text>Product ID: {id}</Text>
      </View>
    </>
  );
}
```

### Styling with StyleSheet
```typescript
import { StyleSheet, View, Text, TouchableOpacity, Platform } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

interface CardProps {
  title: string;
  subtitle?: string;
  onPress: () => void;
}

export function Card({ title, subtitle, onPress }: CardProps) {
  const insets = useSafeAreaInsets();

  return (
    <TouchableOpacity
      style={styles.card}
      onPress={onPress}
      activeOpacity={0.7}
    >
      <Text style={styles.title}>{title}</Text>
      {subtitle && <Text style={styles.subtitle}>{subtitle}</Text>}
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
    marginHorizontal: 16,
    marginVertical: 8,
    // Cross-platform shadow
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 8,
      },
      android: {
        elevation: 4,
      },
    }),
  },
  title: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1a1a1a',
    letterSpacing: -0.3,
  },
  subtitle: {
    fontSize: 14,
    color: '#666666',
    marginTop: 4,
  },
});
```

### Reanimated 3 — Animations
```typescript
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withTiming,
  withRepeat,
  withSequence,
  runOnJS,
  interpolate,
  Extrapolation,
  FadeIn,
  FadeOut,
  SlideInRight,
  useAnimatedScrollHandler,
} from 'react-native-reanimated';
import { Gesture, GestureDetector } from 'react-native-gesture-handler';

// Animated button with scale feedback
export function AnimatedButton({ onPress, children }) {
  const scale = useSharedValue(1);

  const gesture = Gesture.Tap()
    .onBegin(() => {
      scale.value = withSpring(0.95, { damping: 10, stiffness: 400 });
    })
    .onFinalize(() => {
      scale.value = withSpring(1, { damping: 10, stiffness: 400 });
      runOnJS(onPress)();
    });

  const animStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  return (
    <GestureDetector gesture={gesture}>
      <Animated.View style={animStyle}>
        {children}
      </Animated.View>
    </GestureDetector>
  );
}

// Collapsible header on scroll
export function ScrollWithHeader() {
  const scrollY = useSharedValue(0);
  const HEADER_HEIGHT = 200;

  const scrollHandler = useAnimatedScrollHandler({
    onScroll: (event) => {
      scrollY.value = event.contentOffset.y;
    },
  });

  const headerStyle = useAnimatedStyle(() => ({
    height: interpolate(
      scrollY.value,
      [0, HEADER_HEIGHT],
      [HEADER_HEIGHT, 60],
      Extrapolation.CLAMP,
    ),
    opacity: interpolate(
      scrollY.value,
      [0, HEADER_HEIGHT / 2],
      [1, 0],
      Extrapolation.CLAMP,
    ),
  }));

  return (
    <>
      <Animated.View style={[styles.header, headerStyle]}/>
      <Animated.ScrollView onScroll={scrollHandler} scrollEventThrottle={16}>
        {/* content */}
      </Animated.ScrollView>
    </>
  );
}

// Entering/exiting animations
export function AnimatedList({ items }) {
  return items.map((item, index) => (
    <Animated.View
      key={item.id}
      entering={FadeIn.delay(index * 50).duration(300)}
      exiting={FadeOut.duration(200)}
    >
      <ItemComponent item={item} />
    </Animated.View>
  ));
}
```

### Performance — FlashList for Large Lists
```typescript
import { FlashList } from '@shopify/flash-list';
import { Image } from 'expo-image';
import { memo, useCallback } from 'react';

// FlashList is 10x faster than FlatList for large datasets
// It recycles cell components instead of creating new ones

interface Product {
  id: string;
  name: string;
  price: number;
  imageUrl: string;
}

const ProductItem = memo(function ProductItem({ item }: { item: Product }) {
  return (
    <View style={styles.item}>
      <Image
        source={{ uri: item.imageUrl }}
        style={styles.image}
        contentFit='cover'
        placeholder={{ blurhash: 'L6PZfSi_.AyE_3t7t7R**0o#DgR4' }}
        transition={200}
      />
      <Text style={styles.name}>{item.name}</Text>
      <Text style={styles.price}>${item.price}</Text>
    </View>
  );
});

export function ProductList({ products }: { products: Product[] }) {
  const renderItem = useCallback(
    ({ item }: { item: Product }) => <ProductItem item={item} />,
    []
  );

  const keyExtractor = useCallback((item: Product) => item.id, []);

  return (
    <FlashList
      data={products}
      renderItem={renderItem}
      keyExtractor={keyExtractor}
      estimatedItemSize={120}    // critical for FlashList performance
      numColumns={2}
      showsVerticalScrollIndicator={false}
      // Prefetch 10 screens ahead
      overrideItemLayout={(layout, item) => {
        layout.size = 120;
      }}
    />
  );
}
```

### Data Fetching with TanStack Query
```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { View, ActivityIndicator, Text, RefreshControl } from 'react-native';

async function fetchProducts(): Promise<Product[]> {
  const res = await fetch('https://api.example.com/products');
  if (!res.ok) throw new Error('Failed to fetch products');
  return res.json();
}

export function useProducts() {
  return useQuery({
    queryKey: ['products'],
    queryFn: fetchProducts,
    staleTime: 5 * 60 * 1000,  // 5 minutes
  });
}

export function ProductsScreen() {
  const { data, isLoading, isError, error, refetch, isRefetching } = useProducts();

  if (isLoading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size='large' />
      </View>
    );
  }

  if (isError) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <Text>Error: {error.message}</Text>
        <TouchableOpacity onPress={() => refetch()}>
          <Text>Retry</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <FlashList
      data={data}
      renderItem={({ item }) => <ProductItem item={item} />}
      estimatedItemSize={120}
      refreshControl={
        <RefreshControl
          refreshing={isRefetching}
          onRefresh={refetch}
          tintColor='#007AFF'
        />
      }
    />
  );
}

// Mutation with optimistic update
export function useFavoriteProduct() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (productId: string) => favoriteProduct(productId),
    onMutate: async (productId) => {
      await queryClient.cancelQueries({ queryKey: ['products'] });
      const prev = queryClient.getQueryData<Product[]>(['products']);
      queryClient.setQueryData<Product[]>(['products'], (old) =>
        old?.map(p => p.id === productId ? { ...p, favorited: true } : p)
      );
      return { prev };
    },
    onError: (err, variables, context) => {
      queryClient.setQueryData(['products'], context?.prev);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
  });
}
```

### Push Notifications with Expo
```typescript
import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';
import { useEffect, useRef } from 'react';
import { Platform } from 'react-native';

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

export async function registerForPushNotifications(): Promise<string | null> {
  if (!Device.isDevice) {
    console.warn('Push notifications only work on physical devices');
    return null;
  }

  const { status: existingStatus } = await Notifications.getPermissionsAsync();
  let finalStatus = existingStatus;

  if (existingStatus !== 'granted') {
    const { status } = await Notifications.requestPermissionsAsync();
    finalStatus = status;
  }

  if (finalStatus !== 'granted') {
    return null;
  }

  if (Platform.OS === 'android') {
    await Notifications.setNotificationChannelAsync('default', {
      name: 'default',
      importance: Notifications.AndroidImportance.MAX,
      vibrationPattern: [0, 250, 250, 250],
    });
  }

  const token = await Notifications.getExpoPushTokenAsync({
    projectId: 'your-expo-project-id',
  });

  return token.data;
}

export function useNotifications(onReceive?: (notification: any) => void) {
  const notificationListener = useRef<any>();
  const responseListener = useRef<any>();

  useEffect(() => {
    registerForPushNotifications().then(token => {
      if (token) sendTokenToServer(token);
    });

    notificationListener.current = Notifications.addNotificationReceivedListener(
      notification => onReceive?.(notification)
    );

    responseListener.current = Notifications.addNotificationResponseReceivedListener(
      response => handleNotificationTap(response)
    );

    return () => {
      Notifications.removeNotificationSubscription(notificationListener.current);
      Notifications.removeNotificationSubscription(responseListener.current);
    };
  }, []);
}
```

### EAS Build Configuration
```json
{
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": { "simulator": true }
    },
    "preview": {
      "distribution": "internal",
      "ios": { "resourceClass": "m-medium" },
      "android": { "buildType": "apk" }
    },
    "production": {
      "autoIncrement": true,
      "ios": {
        "resourceClass": "m-medium",
        "image": "latest"
      },
      "android": {
        "buildType": "app-bundle"
      }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "your@email.com",
        "ascAppId": "1234567890",
        "appleTeamId": "ABCD123456"
      },
      "android": {
        "serviceAccountKeyPath": "./google-service-account.json",
        "track": "internal"
      }
    }
  }
}

# Build commands
# eas build --platform ios --profile production
# eas build --platform android --profile production
# eas submit --platform ios --profile production
# eas submit --platform android --profile production
# eas update --branch production --message 'Fix button color'  # OTA update
```

---

## Best Practices

- Use Expo unless you have specific native module needs — faster development
- Use FlashList instead of FlatList for any list with more than 50 items
- Use expo-image instead of React Native's Image — better performance and caching
- Run animations on the UI thread with Reanimated — never on JS thread
- Use TanStack Query for server state — not useState + useEffect
- Always handle safe area insets — notches and home indicators vary per device
- Test on real devices regularly — simulator performance is misleading
- Use EAS Build for CI/CD — local builds are slow and inconsistent

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| FlatList for large lists | Janky scrolling, dropped frames | Use FlashList with estimatedItemSize |
| Animations on JS thread | Choppy when JS is busy | Use Reanimated worklets (UI thread) |
| Missing GestureHandlerRootView | Gestures not working | Wrap app root in GestureHandlerRootView |
| No safe area handling | Content behind notch or home bar | Use useSafeAreaInsets or SafeAreaView |
| setState in render | Infinite loop | Move state updates to useEffect or handlers |
| No memo on list items | Re-renders entire list on parent update | Wrap items in memo() |
| Inline functions in JSX | New reference every render breaks memo | useCallback for handlers passed as props |
| Missing estimatedItemSize | FlashList layout warnings and slow render | Always provide estimatedItemSize |

---

## Related Skills

- **react-expert**: For React patterns that apply to React Native
- **typescript-expert**: For TypeScript in React Native
- **ios-expert**: For native iOS integrations
- **android-expert**: For native Android integrations
- **cicd-expert**: For EAS Build CI/CD pipelines
- **appsec-expert**: For mobile app security