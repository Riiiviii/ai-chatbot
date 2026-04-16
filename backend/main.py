from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/chat")
def chat_message(chat_request: ChatRequest):
    return {"message": chat_request.message, "response": "ok"}
