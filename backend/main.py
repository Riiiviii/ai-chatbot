from fastapi import FastAPI
from dotenv import load_dotenv
from agents import Runner
from agent import agent
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


load_dotenv(override=True)
app = FastAPI()


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/chat")
async def chat_message(chat_request: ChatRequest):
    response = await Runner.run(agent, chat_request.message)
    return {"message": chat_request.message, "response": response.final_output}
