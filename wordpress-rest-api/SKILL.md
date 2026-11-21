---
name: wordpress-rest-api
description: Use when designing, building, debugging, or securing custom endpoints, consuming, or auditing the WordPress REST API (wp-json routes, controllers, schemas, authentication, and permission callbacks) in a theme or plugin.
author: Luo Kai
provenance: original
version: 1.0.0
---

# WordPress REST API

## Purpose and boundaries

This skill covers work against the WordPress REST API: registering routes with `register_rest_route`, extending core resources, validating and sanitizing input, enforcing permissions, shaping responses, and consuming endpoints from external clients or server-side code.

In scope: custom plugin/theme endpoints, extending core post types or meta exposure, authentication choices (cookie with nonce, application passwords, OAuth-based plugins), error shapes, pagination, and performance of list endpoints.

Out of scope: front-end block editor internals, WooCommerce-specific REST namespaces beyond general patterns, hosting configuration, and legal or compliance certification of any data flow.

## Inputs and assumptions

Collect before writing code:

- WordPress core version and PHP version. Treat all REST behaviour details as version-sensitive; verify against the current official Developer Handbook for the target release.
- Whether the consumer is browser JavaScript (same origin), a server-to-server client, or a mobile/third-party app.
- Resource type: core object, custom post type, taxonomy, user, options, or non-WordPress data.
- Required operations (read, create, update, delete) and data sensitivity.
- Existing namespace conventions. Use a vendor-specific namespace such as `acme/v1`; never reuse `wp/v2`.

Assume nothing about auth state. Assume production traffic and multisite is possible unless stated otherwise.

## Operating workflow

1. **Map the contract first.** Write the route list: method, path, arguments, response shape, and required capability for each. Get this reviewed before implementation.
2. **Register routes on `rest_api_init`**, never earlier. Call `register_rest_route` with an explicit `methods` value, a `permission_callback` on every route (never omit it; a missing callback triggers a deprecation notice and is a security defect), and an `args` array.
3. **Declare argument schemas.** For each argument set `type`, `required`, `sanitize_callback`, and `validate_callback` or `enum`. Use `sanitize_text_field`, `absint`, `sanitize_key`, or `wp_kses_post` as appropriate to the field.
4. **Implement permission callbacks** using capability checks such as `current_user_can( 'edit_post', $id )` against the specific object, not a blanket `is_user_logged_in()`.
5. **Build responses** with `WP_REST_Response` or return arrays/`WP_Error`. Return only fields the consumer needs; never expose password hashes, internal meta keys, or unfiltered `$wpdb` rows.
6. **Paginate every collection.** Accept `per_page` (cap at 100) and `page`; return `X-WP-Total` and `X-WP-TotalPages` headers.
7. **Expose meta deliberately.** Use `register_post_meta` with `show_in_rest` and an explicit `auth_callback`. Do not set `show_in_rest` on sensitive keys.
8. **Verify** using the checklist below before handing over.

## Decision gates

- **Authentication choice.** Cookie auth plus `X-WP-Nonce` (`wp_rest` action) only for same-origin logged-in browser requests. Application passwords for trusted server-to-server integrations over HTTPS. Anything requiring third-party delegated access: use a vetted OAuth implementation and confirm current support with its documentation.
- **Write operations.** Any endpoint that deletes, overwrites, changes roles, sends email, charges money, or calls an external service requires explicit user approval of the route design and a rollback path before deployment.
- **Public read endpoints.** Allowed only for data already public on the site. Confirm with the data owner.
- **Schema expansion.** Adding fields to core responses via `register_rest_field` or filters is a breaking-change risk for consumers; require a version bump in the namespace for removals or type changes.
- **Heavy queries.** If a list endpoint would exceed roughly 500 ms on realistic data, stop and redesign: add indexed filters, caching, or a dedicated table.

## Verification and evidence

Run and record:

- `curl` or HTTP client requests for each route, showing status codes for: anonymous, under-privileged, authorized, and malformed input. Expected: 401/403 for denied, 400 for invalid arguments, 200/201 for success.
- A check that every registered route has a non-empty `permission_callback` (grep the codebase; no route may lack one).
- Confirmation that unauthenticated `OPTIONS` and `GET` responses contain no fields marked sensitive.
- Pagination test: request page boundaries and verify header totals match a direct query count.
- Response schema comparison against the documented contract, field by field.
- Logs or query monitor output showing no N+1 query pattern on list endpoints (target: query count does not grow linearly with item count).
- Confirm version-sensitive behaviour (argument handling, auth defaults) against the current official documentation and cite the page reviewed.

## Failure handling

- **400 unexpected on valid input:** check `required` and type coercion; numeric strings and booleans are commonly mishandled.
- **403 for admins:** the capability check is on the wrong object or context; test with the exact role.
- **Nonce failures (403 `rest_cookie_invalid_nonce`):** the nonce is stale, missing, or sent for a different action. Re-issue via `wp_create_nonce( 'wp_rest' )` in the rendering context.
- **Route not found:** `rest_api_init` ran too late, the namespace or path has a typo, or permalinks/rewrite rules need flushing after activation. Flush only on activation or after explicit approval.
- **Caching layer serving stale or private responses:** exclude `wp-json` from page caching and never cache authenticated responses publicly.
- If a fix requires changing a published contract, stop and present options to the owner.

## Deliverable contract

Provide:

1. Route contract table: method, path, auth, arguments, response fields, capability.
2. Complete PHP for the registration and callbacks, with no placeholders.
3. Verification log: request/response pairs and results for each checklist item.
4. List of version-sensitive assumptions with the documentation page used to confirm them.
5. Known limitations and any operations awaiting approval.

Do not: expose `show_in_rest` on credentials or personal data without review; use `__return_true` as a permission callback on write routes; disable SSL verification in client code; hardcode secrets in source; or claim compliance with any regulation based on this work.