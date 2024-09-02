from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from dialog import Dialog

class Message(BaseModel):
    content: str
    conversation_id: str | None = None
    
dialog = Dialog()

app = FastAPI()

@app.post("/chat")
def chat(message: Message):
    return {'response': dialog.query(message.content, message.conversation_id)}