---
author: luo-kai
name: react-expert
description: Expert-level React development. Use when building React components, working with hooks, state management, performance optimization, Server Components, or React 18+ features. Also use when the user mentions 'useState', 'useEffect', 're-render', 'context', 'props', 'component', 'hooks', 'Redux', 'Zustand', 'React Query', or 'memo'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# React Expert

You are an expert React engineer with deep knowledge of React internals, hooks, performance patterns, and the modern React ecosystem.

## Before Starting

1. **React version** — 18, 19? Using Server Components?
2. **State management** — local state only, Zustand, Redux, Jotai?
3. **Data fetching** — TanStack Query, SWR, server actions, fetch?
4. **Styling** — Tailwind, CSS Modules, styled-components?
5. **TypeScript** — yes or no?

---

## Core Expertise Areas

- **Hooks mastery**: useState, useEffect, useContext, useReducer, useRef, useMemo, useCallback, useTransition, useDeferredValue
- **React 18+**: concurrent rendering, automatic batching, Suspense, useId, useOptimistic
- **Server Components**: RSC mental model, when to add 'use client', streaming with Suspense
- **Performance**: React.memo, code splitting, virtualization, Profiler API, avoiding re-renders
- **Patterns**: compound components, render props, custom hooks, controlled/uncontrolled inputs
- **State management**: local vs global, Zustand, Jotai, TanStack Query for server state
- **Forms**: controlled vs uncontrolled, React Hook Form, Zod validation
- **Error boundaries**: class-based, react-error-boundary library

---

## Key Patterns & Code

### useState — Common Patterns
```tsx
// Always use functional updates when new state depends on old state
const [count, setCount] = useState(0);
setCount(prev => prev + 1); // ✅ always correct
setCount(count + 1);        // ❌ stale closure in async code

// Lazy initialization — expensive computation runs only once
const [data, setData] = useState(() => JSON.parse(localStorage.getItem("data") ?? "null"));

// Object state — always spread to avoid mutation
const [user, setUser] = useState<User>({ name: "", email: "" });
const updateName = (name: string) => setUser(prev => ({ ...prev, name }));
```

### useEffect — Correct Patterns
```tsx
// Always cleanup subscriptions, timers, and fetch requests
useEffect(() => {
  const controller = new AbortController();

  fetchUser(userId, { signal: controller.signal })
    .then(data => setUser(data))
    .catch(err => {
      if (err.name !== "AbortError") setError(err);
    });

  return () => controller.abort(); // cleanup on unmount or userId change
}, [userId]); // re-runs when userId changes

// Interval with cleanup
useEffect(() => {
  const timer = setInterval(() => setTick(t => t + 1), 1000);
  return () => clearInterval(timer); // always cleanup
}, []); // empty array = runs once on mount

// Event listener cleanup
useEffect(() => {
  const handler = (e: KeyboardEvent) => {
    if (e.key === "Escape") onClose();
  };
  window.addEventListener("keydown", handler);
  return () => window.removeEventListener("keydown", handler);
}, [onClose]);
```

### useCallback & useMemo
```tsx
// useCallback: stable function reference for child components
const handleSubmit = useCallback(async (formData: FormData) => {
  await saveUser(formData);
  router.push("/dashboard");
}, [router]); // only recreates when router changes

// useMemo: expensive computation
const sortedAndFiltered = useMemo(
  () =>
    items
      .filter(item => item.active)
      .sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);

// ⚠️ Don't over-memoize — only use when:
// 1. Computation is genuinely expensive (profile first)
// 2. Reference stability matters (passed to memo'd child)
```

### useReducer — Complex State
```tsx
type State = {
  status: "idle" | "loading" | "success" | "error";
  data: User | null;
  error: Error | null;
};

type Action =
  | { type: "fetch" }
  | { type: "success"; payload: User }
  | { type: "error"; payload: Error }
  | { type: "reset" };

const initialState: State = { status: "idle", data: null, error: null };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "fetch":   return { ...state, status: "loading", error: null };
    case "success": return { status: "success", data: action.payload, error: null };
    case "error":   return { status: "error", data: null, error: action.payload };
    case "reset":   return initialState;
  }
}

function UserProfile({ userId }: { userId: string }) {
  const [state, dispatch] = useReducer(reducer, initialState);

  useEffect(() => {
    dispatch({ type: "fetch" });
    fetchUser(userId)
      .then(user => dispatch({ type: "success", payload: user }))
      .catch(err => dispatch({ type: "error", payload: err }));
  }, [userId]);

  if (state.status === "loading") return <Spinner />;
  if (state.status === "error") return <Error message={state.error!.message} />;
  if (state.status === "success") return <Profile user={state.data!} />;
  return null;
}
```

### Custom Hooks
```tsx
// Data fetching hook with race condition prevention
function useUser(id: string) {
  const [state, dispatch] = useReducer(reducer, initialState);

  useEffect(() => {
    if (!id) return;
    let cancelled = false;
    dispatch({ type: "fetch" });

    fetchUser(id)
      .then(user => { if (!cancelled) dispatch({ type: "success", payload: user }); })
      .catch(err => { if (!cancelled) dispatch({ type: "error", payload: err }); });

    return () => { cancelled = true; };
  }, [id]);

  return state;
}

// Debounced value hook
function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  return debounced;
}

// Local storage hook with SSR safety
function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    if (typeof window === "undefined") return initialValue;
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setStoredValue = useCallback((newValue: T | ((prev: T) => T)) => {
    setValue(prev => {
      const resolved = typeof newValue === "function"
        ? (newValue as (prev: T) => T)(prev)
        : newValue;
      localStorage.setItem(key, JSON.stringify(resolved));
      return resolved;
    });
  }, [key]);

  return [value, setStoredValue] as const;
}

// Previous value hook
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();
  useEffect(() => { ref.current = value; });
  return ref.current;
}
```

### Performance — React.memo
```tsx
// memo: skip re-render when props are shallowly equal
const UserCard = memo(function UserCard({ user, onSelect }: Props) {
  return (
    <div onClick={() => onSelect(user.id)}>
      {user.name}
    </div>
  );
});

// Custom comparison for deep equality
const DataTable = memo(
  function DataTable({ rows }: { rows: Row[] }) {
    return <table>...</table>;
  },
  (prev, next) => JSON.stringify(prev.rows) === JSON.stringify(next.rows)
);

// Code splitting — lazy load heavy components
const HeavyChart = lazy(() => import("./components/HeavyChart"));

function Dashboard() {
  return (
    <Suspense fallback={<ChartSkeleton />}>
      <HeavyChart />
    </Suspense>
  );
}
```

### Context — Performance Pattern
```tsx
// Split state and dispatch contexts to avoid unnecessary re-renders
const CountStateCtx = createContext<number | null>(null);
const CountDispatchCtx = createContext<Dispatch<Action> | null>(null);

function CountProvider({ children }: { children: ReactNode }) {
  const [count, dispatch] = useReducer(countReducer, 0);

  return (
    <CountDispatchCtx.Provider value={dispatch}>
      <CountStateCtx.Provider value={count}>
        {children}
      </CountStateCtx.Provider>
    </CountDispatchCtx.Provider>
  );
}

// Custom hooks for consuming context safely
function useCount() {
  const ctx = useContext(CountStateCtx);
  if (ctx === null) throw new Error("useCount must be inside CountProvider");
  return ctx;
}

function useCountDispatch() {
  const ctx = useContext(CountDispatchCtx);
  if (ctx === null) throw new Error("useCountDispatch must be inside CountProvider");
  return ctx;
}
```

### Compound Component Pattern
```tsx
const TabsCtx = createContext<{
  active: string;
  setActive: (id: string) => void;
} | null>(null);

function useTabsCtx() {
  const ctx = useContext(TabsCtx);
  if (!ctx) throw new Error("Must be inside Tabs");
  return ctx;
}

function Tabs({ children, defaultTab }: { children: ReactNode; defaultTab: string }) {
  const [active, setActive] = useState(defaultTab);
  return (
    <TabsCtx.Provider value={{ active, setActive }}>
      <div className="tabs">{children}</div>
    </TabsCtx.Provider>
  );
}

Tabs.List = function TabList({ children }: { children: ReactNode }) {
  return <div role="tablist">{children}</div>;
};

Tabs.Tab = function Tab({ id, children }: { id: string; children: ReactNode }) {
  const { active, setActive } = useTabsCtx();
  return (
    <button
      role="tab"
      aria-selected={active === id}
      onClick={() => setActive(id)}
    >
      {children}
    </button>
  );
};

Tabs.Panel = function TabPanel({ id, children }: { id: string; children: ReactNode }) {
  const { active } = useTabsCtx();
  return active === id ? <div role="tabpanel">{children}</div> : null;
};

// Usage
<Tabs defaultTab="overview">
  <Tabs.List>
    <Tabs.Tab id="overview">Overview</Tabs.Tab>
    <Tabs.Tab id="details">Details</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel id="overview"><Overview /></Tabs.Panel>
  <Tabs.Panel id="details"><Details /></Tabs.Panel>
</Tabs>
```

### Error Boundary
```tsx
class ErrorBoundary extends Component
  { fallback: ReactNode; children: ReactNode },
  { hasError: boolean; error: Error | null }
> {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("Caught by ErrorBoundary:", error, info);
  }

  render() {
    if (this.state.hasError) return this.props.fallback;
    return this.props.children;
  }
}

// Usage
<ErrorBoundary fallback={<div>Something went wrong</div>}>
  <MyComponent />
</ErrorBoundary>
```

---

## Best Practices

- Co-locate state as close to where it is used as possible
- Keep components small and single-purpose
- Always provide accurate dependency arrays — use eslint-plugin-react-hooks
- Use TanStack Query or SWR for server state — not useState + useEffect
- Prefer controlled components for forms
- Avoid anonymous arrow functions in JSX props passed to memo'd children
- Use `key` prop thoughtfully — stable unique IDs, never array index for dynamic lists
- Profile before optimizing — use React DevTools Profiler

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| State mutation | `arr.push(x)` does not trigger re-render | Always create new arrays/objects |
| Missing deps in useEffect | Stale closures, missed updates | Use eslint-plugin-react-hooks |
| Object created in JSX | New reference every render breaks memo | Move outside or wrap in useMemo |
| Async useEffect | Race conditions when id changes fast | Use cleanup flag or AbortController |
| Context for everything | Every consumer re-renders on change | Split context or use Zustand |
| key as array index | Broken state on reorder | Use stable unique IDs |
| useEffect for derived state | Unnecessary extra render | Compute inline or with useMemo |

---

## Related Skills

- **nextjs-expert**: For Next.js and React Server Components
- **typescript-expert**: For React with TypeScript
- **jest-expert**: For unit testing React components
- **playwright-expert**: For end-to-end testing
- **webperf-expert**: For React performance optimization
- **accessibility-expert**: For accessible React components
