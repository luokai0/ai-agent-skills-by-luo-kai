---
name: skylv-sql-helper
slug: skylv-sql-helper
version: 1.0.0
description: "SQL query builder and optimizer. Generates queries, explains execution plans, and optimizes slow queries. Triggers: sql query, database query, sql optimization."
author: SKY-lv
license: MIT
tags: [automation, tools]
keywords: [automation, tools]
triggers: sql-helper
---

# SQL Helper

## Overview
Helps write, optimize, and debug SQL queries.

## When to Use
- User asks to "write a SQL query" or "optimize this query"
- Debugging slow database operations

## Pagination
SELECT * FROM users ORDER BY id LIMIT 20 OFFSET 40;

## Join with Aggregation
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;

## Optimization Rules
- Add indexes on WHERE/JOIN columns
- Avoid SELECT * - specify columns
- Use EXPLAIN to analyze execution plan
- Optimize JOIN order (small table first)
- Add LIMIT for pagination

## Anti-Patterns to Avoid
- SELECT * in production code
- Nested subqueries (use JOINs or CTEs)
- OR in WHERE clause (use IN or UNION)
