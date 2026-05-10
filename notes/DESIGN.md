# Design Notes

Decisions made during initial development, with reasoning preserved for
future reference. Captures intentional v1 scope and the conditions under
which each decision should be revisited.

## Request/response shape

`ChatRequest` and `ChatResponse` are intentionally minimal: a message
string in, a response string out.

The user message is not echoed in the response payload. The frontend
already holds the input it sent, and the locked-input UI guarantees only
one in-flight request at a time, so request-response matching is implicit.

**Revisit if:** the UI moves away from locked-input semantics, or
streaming/concurrent requests are introduced. At that point a
`request_id` field becomes the right pattern, not echoing the message.

## Conversation memory

The `/chat` endpoint is currently stateless. Each request runs the agent
with no prior context.

Memory is deferred until after deployment. Designing it well requires
decisions on:

- Storage backend (in-memory dict, Redis, Postgres, SQLite)
- Conversation ID generation (client UUID, server-issued, auth-derived)
- Session lifetime (forever, 24h, browser session)
- Token budget strategy when history grows past the model's context
  window (truncation, summarisation, sliding window)
- Per-conversation isolation: the server holds histories keyed by
  conversation ID, not the client. The client sends only the
  conversation ID and the new message.

**Revisit when:** the stateless chatbot is deployed and live. Memory
becomes the next feature, scoped as its own work.

## Agent instance scoping

A single shared `GraduateAgent` instance lives on `app.state` and is used
for every request. This works for stateless chat, but breaks the moment
per-user conversation history is introduced.

**Revisit when:** memory is added. Either create a fresh agent per
request, or keep the shared agent and pass per-session message history
into `Runner.run()`. The Agents SDK is designed for the latter.

## Configuration

Environment variables are loaded via a hand-rolled `Settings` class in
`settings.py`. Currently exposes `mcp_server_url` and `cors_origins`,
both with sensible local-development defaults. Comma-separated env vars
are split and stripped of whitespace at load time.

**Revisit when:** the env var count grows past ~5, validation becomes
non-trivial (typed values, optional vs required complexity), or
inter-service config is introduced. At that point migrate to
`pydantic-settings` (`BaseSettings`) — same library family already in
use for request/response models.

## CORS configuration

`CORSMiddleware` allows `GET` and `POST` from configured origins, with
`allow_credentials=False` and `allow_headers=["*"]`. The chatbot is
stateless and uses no cookie or session-based auth, so credentials are
deliberately disabled.

`allow_headers=["*"]` is acceptable for v1 because the only route
accepts a JSON body validated by Pydantic — header content does not
influence handler logic.

**Revisit if:** authentication is introduced (credentials may need to
become `True` and origins must remain exact rather than wildcard), or
sensitive endpoints are added that warrant least-privilege header
restriction (`["Content-Type", "Authorization"]`).

## Schemas directory

Pydantic models live in `schemas/` grouped by domain (`schemas/chat.py`).
Models are kept here rather than alongside their consuming routes, to
prepare for reuse as the project adds endpoints.

**Revisit if:** the project remains at one schema file for a long time
and the directory feels like over-structure. For now, the structure is
preserved in anticipation of additional endpoints.

## Out of scope for v1

- Authentication (no user accounts; chatbot is public)
- Rate limiting (acceptable risk for a portfolio project)
- Streaming responses (tokens delivered as one block)
- Multi-agent orchestration (single agent only)
- Observability beyond standard logging
