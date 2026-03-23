---
author: luo-kai
name: nextjs-expert
description: Expert-level Next.js development. Use when building Next.js apps, working with App Router, Server Components, Client Components, Server Actions, data fetching, middleware, ISR, SSG, SSR, or deploying Next.js. Also use when the user mentions 'App Router', 'Server Actions', 'getServerSideProps', 'middleware', 'ISR', 'use client', 'use server', 'layout.tsx', or 'page.tsx'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Next.js Expert

You are an expert Next.js engineer with deep knowledge of the App Router, React Server Components, caching layers, and production deployment patterns.

## Before Starting

1. **Next.js version** — 13, 14, or 15?
2. **Router** — App Router or Pages Router?
3. **Deployment** — Vercel, self-hosted Node.js, Docker, edge?
4. **Data fetching** — database direct, REST API, GraphQL?
5. **Auth** — NextAuth, Clerk, Auth.js, custom?

---

## Core Expertise Areas

- **App Router**: layout hierarchy, nested layouts, route groups, parallel routes, intercepting routes
- **Server vs Client Components**: mental model, when to add 'use client', serialization rules
- **Data fetching**: fetch with caching, generateStaticParams, dynamic rendering triggers
- **Server Actions**: forms, useFormState, useFormStatus, optimistic updates with useOptimistic
- **Caching layers**: Request Memoization, Data Cache, Full Route Cache, Router Cache — all four
- **Middleware**: matcher config, request rewriting, auth patterns, edge runtime limits
- **Metadata API**: static and dynamic metadata, Open Graph, Twitter cards
- **Performance**: partial prerendering, streaming, Suspense boundaries, image optimization

---

## Key Patterns & Code

### App Router File Structure
```
app/
  layout.tsx              # Root layout — wraps all pages
  page.tsx                # Home page /
  loading.tsx             # Loading UI (automatic Suspense)
  error.tsx               # Error UI (automatic Error Boundary)
  not-found.tsx           # 404 page
  (auth)/                 # Route group — no URL segment
    login/
      page.tsx            # /login
    register/
      page.tsx            # /register
  dashboard/
    layout.tsx            # Nested layout for /dashboard/*
    page.tsx              # /dashboard
    @modal/               # Parallel route slot
      (..)photo/[id]/
        page.tsx          # Intercepting route
    [userId]/
      page.tsx            # /dashboard/123
    [...slug]/
      page.tsx            # /dashboard/a/b/c
lib/
  actions.ts              # Server Actions
  db.ts                   # Database client (singleton)
  auth.ts                 # Auth helpers
components/
  ui/                     # Shared UI components
```

### Server vs Client Components
```tsx
// SERVER COMPONENT (default) — runs on server only
// ✅ Can: async/await, access DB directly, use secrets
// ❌ Cannot: useState, useEffect, event handlers, browser APIs

// app/users/page.tsx
import { db } from "@/lib/db";

export default async function UsersPage() {
  // Direct DB access — no API needed
  const users = await db.user.findMany({
    orderBy: { createdAt: "desc" },
    take: 20,
  });

  return (
    <div>
      <h1>Users</h1>
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
}

// CLIENT COMPONENT — runs on server (for HTML) AND client
// ✅ Can: useState, useEffect, event handlers, browser APIs
// ❌ Cannot: async/await at component level, access secrets

"use client";

import { useState } from "react";

export function SearchBar({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState("");

  return (
    <input
      value={query}
      onChange={e => setQuery(e.target.value)}
      onKeyDown={e => e.key === "Enter" && onSearch(query)}
      placeholder="Search..."
    />
  );
}
```

### Data Fetching & Caching
```tsx
// fetch with caching options
async function getData(id: string) {
  // Static — cached indefinitely (default in static rendering)
  const static_data = await fetch(`https://api.example.com/static/${id}`);

  // Revalidate every 60 seconds (ISR equivalent)
  const revalidated = await fetch(`https://api.example.com/posts`, {
    next: { revalidate: 60 },
  });

  // Dynamic — never cache (always fresh)
  const dynamic_data = await fetch(`https://api.example.com/live/${id}`, {
    cache: "no-store",
  });

  return { static_data, revalidated, dynamic_data };
}

// Parallel data fetching — don't await sequentially
export default async function Page({ params }: { params: { id: string } }) {
  // ✅ Start both fetches simultaneously
  const [user, posts] = await Promise.all([
    getUser(params.id),
    getUserPosts(params.id),
  ]);

  return <Profile user={user} posts={posts} />;
}

// generateStaticParams — pre-render dynamic routes at build time
export async function generateStaticParams() {
  const posts = await db.post.findMany({ select: { slug: true } });
  return posts.map(post => ({ slug: post.slug }));
}
```

### Streaming with Suspense
```tsx
// app/dashboard/page.tsx
import { Suspense } from "react";

// Page renders immediately with shell
// Slow components stream in when ready
export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>

      {/* Renders immediately — no async */}
      <QuickStats />

      {/* Streams in after slow DB query */}
      <Suspense fallback={<RevenueChartSkeleton />}>
        <RevenueChart />    {/* async Server Component */}
      </Suspense>

      {/* Streams in independently */}
      <Suspense fallback={<ActivityFeedSkeleton />}>
        <ActivityFeed />    {/* async Server Component */}
      </Suspense>
    </div>
  );
}

// Async Server Component
async function RevenueChart() {
  // This slow query doesn't block the rest of the page
  const data = await db.order.aggregate({
    _sum: { total: true },
    groupBy: ["month"],
  });
  return <Chart data={data} />;
}
```

### Server Actions
```tsx
// lib/actions.ts
"use server";

import { revalidatePath, revalidateTag } from "next/cache";
import { redirect } from "next/navigation";
import { z } from "zod";

const CreatePostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(10),
  published: z.boolean().default(false),
});

export async function createPost(formData: FormData) {
  // Validate
  const parsed = CreatePostSchema.safeParse({
    title: formData.get("title"),
    content: formData.get("content"),
    published: formData.get("published") === "on",
  });

  if (!parsed.success) {
    return { error: parsed.error.flatten().fieldErrors };
  }

  // Authorize
  const session = await getSession();
  if (!session) return { error: { _form: ["Unauthorized"] } };

  // Mutate
  const post = await db.post.create({
    data: { ...parsed.data, authorId: session.userId },
  });

  // Revalidate cache
  revalidatePath("/posts");
  revalidateTag("posts");

  // Redirect
  redirect(`/posts/${post.id}`);
}

// With useFormState for error display
"use client";
import { useFormState, useFormStatus } from "react-dom";
import { createPost } from "@/lib/actions";

const initialState = { error: null };

export function CreatePostForm() {
  const [state, formAction] = useFormState(createPost, initialState);

  return (
    <form action={formAction}>
      <input name="title" placeholder="Title" />
      {state.error?.title && <p>{state.error.title[0]}</p>}

      <textarea name="content" placeholder="Content" />
      {state.error?.content && <p>{state.error.content[0]}</p>}

      <SubmitButton />
    </form>
  );
}

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending}>
      {pending ? "Creating..." : "Create Post"}
    </button>
  );
}
```

### Middleware
```typescript
// middleware.ts (root of project)
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Auth check
  const token = request.cookies.get("session")?.value;
  const isAuthenticated = !!token; // validate token here

  const isProtectedRoute = pathname.startsWith("/dashboard");
  const isAuthRoute = pathname.startsWith("/login");

  if (isProtectedRoute && !isAuthenticated) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  if (isAuthRoute && isAuthenticated) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  // Add request headers for downstream use
  const requestHeaders = new Headers(request.headers);
  requestHeaders.set("x-pathname", pathname);

  return NextResponse.next({
    request: { headers: requestHeaders },
  });
}

// Only run middleware on these paths
export const config = {
  matcher: [
    "/((?!api|_next/static|_next/image|favicon.ico).*)",
  ],
};
```

### Metadata API
```tsx
// Static metadata
export const metadata: Metadata = {
  title: "My App",
  description: "My app description",
  openGraph: {
    title: "My App",
    description: "My app description",
    images: ["/og-image.png"],
  },
};

// Dynamic metadata
export async function generateMetadata(
  { params }: { params: { id: string } }
): Promise<Metadata> {
  const post = await getPost(params.id);
  if (!post) return { title: "Not Found" };

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
    },
  };
}
```

### The Four Caching Layers
```
1. Request Memoization (per-render)
   - Deduplicates identical fetch() calls in the same render tree
   - Automatic — no configuration needed
   - Resets after each server request

2. Data Cache (persistent)
   - Stores fetch() responses on the server
   - Controlled by: cache: 'no-store' | next: { revalidate: N } | next: { tags: [] }
   - Persists across deployments until revalidated

3. Full Route Cache (build time)
   - Caches rendered HTML + RSC payload of static routes
   - Opt out with: export const dynamic = 'force-dynamic'
   - Revalidated with: revalidatePath() or revalidateTag()

4. Router Cache (client-side)
   - Caches RSC payloads in browser memory
   - Lasts 30s (dynamic) or 5min (static) by default
   - Cleared on: router.refresh() or server action completion
```

---

## Best Practices

- Default to Server Components — only add `use client` when needed
- Fetch data as close to where it's used as possible — in the Server Component itself
- Use `Promise.all()` for parallel fetches — never sequential awaits
- Put Suspense boundaries around slow async components for streaming
- Use Server Actions for mutations — not API routes in App Router
- Validate and authorize in every Server Action — never trust the client
- Use `revalidatePath` or `revalidateTag` after mutations
- Use `next/image` for all images — automatic optimization
- Use `next/font` for fonts — eliminates layout shift

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| `use client` at top of tree | Entire subtree becomes client | Push `use client` as far down as possible |
| Sequential awaits | Waterfall data fetching | Use Promise.all() for parallel fetches |
| Secrets in Client Components | Exposed to browser | Only use secrets in Server Components |
| Missing Suspense boundaries | Page blocks on slow data | Wrap async components in Suspense |
| Mutating in Server Component | Should only read in RSC | Use Server Actions for mutations |
| No revalidation after mutation | Stale UI after action | Call revalidatePath/revalidateTag |
| fetch in Client Component | Exposes API routes unnecessarily | Fetch in Server Component, pass as props |

---

## Related Skills

- **react-expert**: For React hooks and patterns
- **typescript-expert**: For Next.js type safety
- **postgresql-expert**: For database with Next.js
- **auth-expert**: For authentication patterns
- **webperf-expert**: For Next.js performance optimization
- **docker-expert**: For self-hosting Next.js
