import os
from agents import Runner
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from graduate_agent import GraduateAgent
from agents.mcp import MCPServerSse, MCPServerSseParams
from schemas.chat import ChatRequest, ChatResponse

load_dotenv(override=True)


server_params = MCPServerSseParams(url=os.getenv("URL", "http://localhost:8001/sse"))


@asynccontextmanager
async def lifespan(application: FastAPI):
    async with MCPServerSse(server_params) as server:
        application.state.agent = GraduateAgent().create_agent([server])
        yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat_message(chat_request: ChatRequest, request: Request) -> ChatResponse:
    agent = request.app.state.agent
    result = await Runner.run(agent, chat_request.message)
    return ChatResponse(response=result.final_output)
