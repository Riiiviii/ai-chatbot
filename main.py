from agents import Runner
from settings import settings
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from agent import GraduateAgent
from agents.mcp import MCPServerSse, MCPServerSseParams
from schemas.chat import ChatRequest, ChatResponse
from fastapi.middleware.cors import CORSMiddleware

server_params = MCPServerSseParams(url=settings.mcp_server_url)


@asynccontextmanager
async def lifespan(application: FastAPI):
    async with MCPServerSse(server_params) as server:
        application.state.agent = GraduateAgent().create_agent([server])
        yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat_message(chat_request: ChatRequest, request: Request) -> ChatResponse:
    agent = request.app.state.agent
    result = await Runner.run(agent, chat_request.message)
    return ChatResponse(response=result.final_output)
