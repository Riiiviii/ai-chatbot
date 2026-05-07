from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from agents import Runner
from agent import create_agent
from pydantic import BaseModel
from agents.mcp import MCPServerSse, MCPServerSseParams


load_dotenv(override=True)


class ChatRequest(BaseModel):
    message: str


server_params = MCPServerSseParams(url="http://localhost:8001/sse")


@asynccontextmanager
async def lifespan(application: FastAPI):
    async with MCPServerSse(server_params) as server:
        application.state.agent = create_agent([server])
        yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/chat")
async def chat_message(chat_request: ChatRequest, request: Request):
    agent = request.app.state.agent
    response = await Runner.run(agent, chat_request.message)
    return {"message": chat_request.message, "response": response.final_output}
