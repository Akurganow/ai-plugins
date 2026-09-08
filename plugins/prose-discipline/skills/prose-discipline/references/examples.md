# Examples: Calibration Corpus

Before/after pairs for calibrating audits. When reporting a finding, name
the closest pattern from this corpus instead of describing the smell in the
abstract. The "before" specimens quote banned patterns and are exempt by
the core contract.

## Review comment

Before:

> I think it might perhaps be slightly better if we didn't perform this
> database query inside the loop because it could potentially lead to some
> performance degradation.

After:

> `issue (blocking):` This query runs inside the loop, causing an N+1 query
> pattern on a 10k-row page. Fetch all IDs upfront and query once with
> `WHERE id IN (...)`.

## Change description

Specimens quote PR descriptions; the same shape holds for release
notes, migration notes, and handoff summaries.

Before:

> In this PR, we have spent significant effort revamping the authentication
> module to seamlessly integrate with our new provider and fix several
> intermittent bugs that our team noticed.

After:

> **What changed:** Replace the custom OAuth handler with the standard
> provider adapter. Drop the hand-rolled token refresh.
> **Why:** the custom handler deadlocks the refresh timer in background
> jobs, producing the intermittent 401s seen in #1421.
> **Verification:** `npm test auth/` green. 24h soak on staging with zero
> refresh failures.

Session-process narrative:

Before:

> **Verification:** an independent verification agent reviewed the
> full change and returned verdict: PASS after adversarial review.

After:

> **Verification:** `npm test auth/` green.

Template precedence:

Before:

> **What changed**
> - Replace the OAuth handler with the provider adapter.
> **Why**
> - Fixes #1421.
> **Verification**
> - `npm test auth/` green.
>
> Written above the template's own "Summary" and "Test plan" fields,
> which stay empty.

After:

> **Summary** (template field)
> Replaces the custom OAuth handler with the standard provider
> adapter. Fixes the refresh deadlock from #1421.
>
> **Test plan** (template field)
> `npm test auth/` green.
>
> The same content inside the template's fields, nothing added on top.

## Error message

Before:

> Oops! Something went wrong while attempting to establish a connection.
> Please verify your settings or contact support if the issue persists.

After:

> Connection to Postgres failed: authentication rejected for user `app`.
> Verify `DB_PASSWORD` in `.env` and retry.

## Code comments

Before:

```ts
// This function handles the validation of the user payload. It first
// checks the schema and then returns the result.
// should work for most cases
```

After: delete both lines. The name `validateUserPayload` states the what.
The hedge is a correctness smell.

Before:

```ts
// --- Helper Functions ---
```

After: delete. Extract the helpers into a module if the boundary matters.

## Sentences

Before: "State is maintained by the request handler, and each update is
validated against the current schema and, if the payload is consistent, the
write is forwarded to the primary store and the replica is notified."

After: "The request handler maintains state. It validates each update
against the current schema. Consistent payloads are written to the primary
store. The replica is notified after the write."

## Noun stack

Before: "the service cluster event bus message priority handler".

After: "the handler that sets event priority on the service cluster's event
bus".
