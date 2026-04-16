from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv(override=True)
app = FastAPI()


class ChatRequest(BaseModel):
    message: str


MODEL = "gpt-4o-mini"
INSTRUCTIONS = """ Your name is Gabriel Riven Wahnich, one first name, two last names.
You are a recently graduated student from RMIT University who completed a bachelor of Computer Science with Distinction"""

agent = Agent(
    name="graduate-agent",
    instructions=INSTRUCTIONS,
    model=MODEL,
)


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/chat")
async def chat_message(chat_request: ChatRequest):
    response = await Runner.run(agent, chat_request.message)
    return {"message": chat_request.message, "response": response.final_output}
