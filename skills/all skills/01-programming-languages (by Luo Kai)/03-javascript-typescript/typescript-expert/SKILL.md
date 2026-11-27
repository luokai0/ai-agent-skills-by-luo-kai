---
author: luo-kai
name: typescript-expert
description: Expert-level TypeScript. Use when working with TypeScript types, generics, conditional types, mapped types, tsconfig, strict mode, type narrowing, utility types, or migrating JS to TS. Also use when the user mentions 'type error', 'any type', 'generic', 'declaration file', 'tsconfig', 'strict mode', 'type narrowing', or 'utility types'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# TypeScript Expert

You are an expert TypeScript engineer who leverages the full power of TypeScript's type system to write safe, maintainable, production-grade code.

## Before Starting

1. **Project type** — Next.js app, Node.js API, library, CLI?
2. **Strict mode** — already enabled? Should we enable it now?
3. **Existing patterns** — what's already in the codebase?
4. **Target** — ES2020+? What module resolution (NodeNext, Bundler)?

---

## Core Expertise Areas

- **Generics**: constraints, defaults, inference, generic classes and interfaces
- **Conditional types**: `extends`, `infer` keyword, distributive conditionals
- **Mapped types**: key remapping, modifiers (`-readonly`, `-?`), template literal keys
- **Template literal types**: string manipulation at the type level
- **Discriminated unions**: exhaustive type checking with switch/if-else
- **Branded types**: nominal typing for IDs and domain values
- **Declaration files**: `.d.ts`, module augmentation, global types
- **tsconfig**: strict options explained, module resolution, paths aliasing

---

## Key Patterns & Code

### tsconfig.json — Production Setup
```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2022"],
    "outDir": "dist",
    "rootDir": "src",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

### Generics
```typescript
// Constrained generics
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Generic with default type parameter
type ApiResponse<T = unknown> = {
  data: T;
  status: number;
  message: string;
};

// Generic class
class Repository<T extends { id: string }> {
  private items = new Map<string, T>();

  save(item: T): void {
    this.items.set(item.id, item);
  }

  findById(id: string): T | undefined {
    return this.items.get(id);
  }

  findAll(): T[] {
    return Array.from(this.items.values());
  }
}
```

### Conditional Types & Infer
```typescript
// Extract inner types using infer
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;
type ArrayElement<T> = T extends (infer E)[] ? E : never;
type ReturnType<T> = T extends (...args: never[]) => infer R ? R : never;
type FirstParam<T> = T extends (first: infer F, ...rest: never[]) => unknown ? F : never;

// Distributive conditional types
type ToArray<T> = T extends unknown ? T[] : never;
type Result = ToArray<string | number>; // string[] | number[]

// Deep readonly
type DeepReadonly<T> = T extends (infer U)[]
  ? ReadonlyArray<DeepReadonly<U>>
  : T extends object
  ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
  : T;
```

### Mapped Types
```typescript
// Built-in utility types re-implemented for learning
type MyPartial<T> = { [K in keyof T]?: T[K] };
type MyRequired<T> = { [K in keyof T]-?: T[K] };
type MyReadonly<T> = { readonly [K in keyof T]: T[K] };
type Mutable<T> = { -readonly [K in keyof T]: T[K] };
type Nullable<T> = { [K in keyof T]: T[K] | null };

// Filter keys by value type
type KeysOfType<T, V> = {
  [K in keyof T]: T[K] extends V ? K : never;
}[keyof T];

type StringKeys = KeysOfType
  { a: string; b: number; c: string },
  string
>; // "a" | "c"

// Rename keys with template literals
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};
type UserGetters = Getters<{ name: string; age: number }>;
// { getName: () => string; getAge: () => number }
```

### Template Literal Types
```typescript
type EventName<T extends string> = `on${Capitalize<T>}`;
type ClickEvent = EventName<"click">; // "onClick"

// Extract route params
type RouteParam<T extends string> =
  T extends `${string}:${infer P}/${string}`
    ? P | RouteParam<`${string}/${string}`>
    : T extends `${string}:${infer P}`
    ? P
    : never;

type Params = RouteParam<"/users/:userId/posts/:postId">;
// "userId" | "postId"
```

### Branded Types
```typescript
// Prevent mixing up IDs of different entities
type Brand<T, B extends string> = T & { readonly __brand: B };

type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;
type Email = Brand<string, "Email">;

const toUserId = (id: string): UserId => id as UserId;
const toOrderId = (id: string): OrderId => id as OrderId;
const toEmail = (raw: string): Email => {
  if (!raw.includes("@")) throw new Error("Invalid email");
  return raw as Email;
};

function getUser(id: UserId): Promise<User> { /* ... */ }

const orderId = toOrderId("abc-123");
getUser(orderId); // ❌ TypeScript Error: OrderId is not UserId
```

### Discriminated Unions
```typescript
// State machine pattern — exhaustive type checking
type RequestState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

function render<T>(state: RequestState<T>): string {
  switch (state.status) {
    case "idle":    return "Idle";
    case "loading": return "Loading...";
    case "success": return `Data: ${JSON.stringify(state.data)}`; // data is T
    case "error":   return `Error: ${state.error.message}`; // error is Error
    // TypeScript will warn if a case is missing — exhaustive checking
  }
}

// Result type for explicit error handling
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function divide(a: number, b: number): Result<number> {
  if (b === 0) return { ok: false, error: new Error("Division by zero") };
  return { ok: true, value: a / b };
}

const result = divide(10, 0);
if (result.ok) {
  console.log(result.value); // number
} else {
  console.error(result.error.message); // Error
}
```

### Type Guards
```typescript
// Custom type guard function
function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    typeof (value as any).id === "string" &&
    "email" in value
  );
}

// Assertion function
function assertIsString(val: unknown): asserts val is string {
  if (typeof val !== "string") {
    throw new TypeError(`Expected string, got ${typeof val}`);
  }
}

// Handle unknown errors safely
function getErrorMessage(error: unknown): string {
  if (error instanceof Error) return error.message;
  if (typeof error === "string") return error;
  return "An unknown error occurred";
}
```

### satisfies Operator (TS 4.9+)
```typescript
// Validate type without widening — best of both worlds
const palette = {
  red: [255, 0, 0],
  green: "#00ff00",
  blue: [0, 0, 255],
} satisfies Record<string, string | number[]>;

// palette.red is still number[], not string | number[]
palette.red.map(x => x * 2);     // ✅ works
palette.green.toUpperCase();      // ✅ works

// Config objects — validate shape without losing specific types
const config = {
  port: 3000,
  host: "localhost",
  debug: true,
} satisfies Record<string, string | number | boolean>;
// config.port is number, not string | number | boolean
```

### Module Augmentation
```typescript
// Extend Express Request
declare module "express" {
  interface Request {
    user?: AuthenticatedUser;
    requestId: string;
    startTime: number;
  }
}

// Add properties to global Window
declare global {
  interface Window {
    analytics: AnalyticsInstance;
    __APP_VERSION__: string;
  }
}

// Ambient declaration for non-TS assets
declare module "*.svg" {
  const content: string;
  export default content;
}

declare module "*.png" {
  const src: string;
  export default src;
}
```

---

## Best Practices

- Always enable `strict: true` in tsconfig — no exceptions
- Prefer `unknown` over `any` — use type guards to narrow
- Use `satisfies` to validate objects without widening their types
- Export types with `export type { ... }` for clarity and tree-shaking
- Enable `noUncheckedIndexedAccess` — array[i] can be undefined
- Enable `exactOptionalPropertyTypes` — `{x?: string}` vs `{x: string | undefined}`
- Run `tsc --noEmit` in CI to catch all type errors without emitting files
- Use `as const` for literal types in arrays and objects

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| `as any` | Defeats type safety entirely | Use `unknown` + type guards |
| Overusing `as Type` | Assertion may be wrong at runtime | Prefer type guards with `is` |
| `!` non-null assertion | Can throw at runtime | Check explicitly with `if` |
| Missing `strict` mode | Many errors go undetected | Enable `strict: true` always |
| `object` type | No property access allowed | Use `Record<string, unknown>` |
| Ignoring `noUncheckedIndexedAccess` | Array access returns `T`, not `T \| undefined` | Enable + handle undefined |
| Circular type references | Stack overflow in type checker | Break cycle with interface or lazy type |

---

## Related Skills

- **react-expert**: For React and TypeScript patterns together
- **nextjs-expert**: For Next.js type-safe development
- **nodejs-expert**: For Node.js TypeScript setup
- **api-design-expert**: For type-safe API design patterns
- **jest-expert**: For testing TypeScript code
