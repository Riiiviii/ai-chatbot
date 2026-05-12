# AI Chatbot — Portfolio Resume Assistant

A FastAPI backend powering an AI chatbot that answers questions about Gabriel Riven Wahnich's professional background. The agent uses the OpenAI Agents SDK with tool-calling via the Model Context Protocol (MCP) to ground responses in structured resume data rather than hallucinating.

This service is consumed by my personal portfolio site over HTTP.

## How it works

1. A user sends a message to `POST /chat`
2. The `GraduateAgent` (`gpt-4o-mini`) receives the message along with a system prompt defining its persona and constraints
3. The agent calls MCP tools to fetch relevant resume data
4. The agent returns a concise, conversational response

The MCP server (`mcp_server.py`) exposes seven tools backed by `resume.json` — covering profile, experience, technical skills, education, social profiles, references, and interests — giving the agent factual data to draw from instead of relying on the model's parametric knowledge.

## Tech stack

| Layer           | Technology                                |
| --------------- | ----------------------------------------- |
| Language        | Python 3.12                               |
| Web framework   | FastAPI                                   |
| Agent runtime   | OpenAI Agents SDK (`openai-agents`)       |
| Tool protocol   | FastMCP (Model Context Protocol)          |
| Model           | `gpt-4o-mini`                             |
| Package manager | uv                                        |
| Container       | Docker (multi-process: FastAPI + FastMCP) |

## Project structure

```
ai-chatbot/
├── main.py          # FastAPI app, lifespan, routes
├── agent.py         # GraduateAgent wrapper
├── mcp_server.py    # FastMCP server exposing resume tools
├── settings.py      # Env-based configuration
├── prompt.txt       # Agent system prompt
├── resume.json      # Structured resume data (source of truth)
├── entrypoint.sh    # Container start script — boots both processes
├── Dockerfile       # Image definition
├── .dockerignore    # Excluded paths from build context
├── schemas/
│   └── chat.py      # ChatRequest / ChatResponse Pydantic models
└── DESIGN.md        # v1 design decisions and trade-offs
```

## Setup

**Prerequisites:** Docker, an [OpenAI API key](https://platform.openai.com/api-keys)

```bash
cp .env.example .env
# Then fill in OPENAI_API_KEY in .env
```

**Environment variables:**

| Variable         | Default                     | Description                     |
| ---------------- | --------------------------- | ------------------------------- |
| `OPENAI_API_KEY` | —                           | Your OpenAI API key (required)  |
| `MCP_SERVER_URL` | `http://localhost:8001/sse` | MCP server SSE endpoint         |
| `CORS_ORIGINS`   | `http://localhost:5173`     | Comma-separated allowed origins |

## Running

The container runs both the FastAPI app and the FastMCP server together via `entrypoint.sh`.

```bash
docker build -t ai-chatbot .
docker run --rm -p 8000:8000 --env-file .env ai-chatbot
```

The API will be available at `http://localhost:8000`.

### Running without Docker (development)

For local iteration without rebuilding the image on every change:

```bash
# Prerequisites: Python 3.12+, uv
uv sync

# Terminal 1 — MCP server
uv run mcp_server.py

# Terminal 2 — FastAPI app with auto-reload
uv run fastapi dev main.py
```

## API

### `GET /`

Health check.

```json
{ "status": "ok" }
```

### `POST /chat`

Send a message to the agent.

**Request:**

```json
{ "message": "What did Gabriel study?" }
```

**Response:**

```json
{ "response": "<TODO: paste a real example response from your testing>" }
```

**Error responses:**

- `422` — invalid input (empty or missing `message`)
- `502` — upstream failure (OpenAI API or MCP server unreachable)

## Design decisions

See [DESIGN.md](DESIGN.md) for documented v1 trade-offs, including why conversation memory is deferred, why a single shared agent instance is used, why both processes run in one container, and what's explicitly out of scope.

## License

MIT — see [LICENSE](LICENSE).
