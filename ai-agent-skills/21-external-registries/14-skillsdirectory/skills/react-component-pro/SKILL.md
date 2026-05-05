---
name: react-component-pro
description: Build reusable, accessible, performant React components with hooks, composition patterns, and modern best practices. Use when building React UIs, creating component libraries, or optimizing React performance.
license: CC0-1.0
compatibility: Works with Cursor, Windsurf, GitHub Copilot, Claude Code, and any AI coding assistant
metadata:
  author: skillsdirectory
  version: "1.0"
  category: web-development
  tools: cursor, windsurf, copilot, claude-code
---

# React Component Pro

You build production-grade React components that are reusable, accessible, and performant.

## Component Principles

1. **Composition over inheritance** — Build with small, composable pieces
2. **Single responsibility** — One component, one purpose
3. **Props down, events up** — Data flows down, actions flow up
4. **Controlled > Uncontrolled** — Parent controls state when possible
5. **Accessibility first** — ARIA attributes, keyboard navigation, semantic HTML

## Component Patterns

### Compound Components
```tsx
<Select value={value} onChange={onChange}>
  <Select.Trigger>Choose option</Select.Trigger>
  <Select.Content>
    <Select.Item value="a">Option A</Select.Item>
    <Select.Item value="b">Option B</Select.Item>
  </Select.Content>
</Select>
```

### Custom Hooks
```tsx
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value)
  
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay)
    return () => clearTimeout(timer)
  }, [value, delay])
  
  return debouncedValue
}
```

### Render Props / Children as Function
```tsx
<DataFetcher url="/api/users">
  {({ data, loading, error }) => (
    loading ? <Spinner /> : <UserList users={data} />
  )}
</DataFetcher>
```

## Performance Optimization

| Problem | Solution |
|---|---|
| Unnecessary re-renders | `React.memo`, `useMemo`, `useCallback` |
| Heavy computations | `useMemo` with proper deps |
| Large lists | Virtualization (react-window) |
| Code splitting | `React.lazy` + `Suspense` |
| State updates causing full re-render | Local state, context splitting |

## TypeScript Patterns for Components

```tsx
// Props with children
interface CardProps {
  title: string
  variant?: 'default' | 'outlined' | 'elevated'
  children: React.ReactNode
}

// Forwarded ref
const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, ...props }, ref) => (
    <div>
      <label>{label}</label>
      <input ref={ref} {...props} />
    </div>
  )
)

// Generic component
interface ListProps<T> {
  items: T[]
  renderItem: (item: T) => React.ReactNode
}
```

## Accessibility Checklist
- [ ] Semantic HTML (`button` not `div onClick`)
- [ ] ARIA labels for interactive elements
- [ ] Keyboard navigation (Tab, Enter, Escape)
- [ ] Focus management (modals, dropdowns)
- [ ] Color contrast ≥ 4.5:1
- [ ] Screen reader tested
