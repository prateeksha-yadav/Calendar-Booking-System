from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import app as agent_app
import os

print("---- CHECKING ENVIRONMENT ----")
print(f"GOOGLE_API_KEY Loaded: {'GOOGLE_API_KEY' in os.environ}")
print(f"GOOGLE_CREDENTIALS_JSON Loaded: {'GOOGLE_CREDENTIALS_JSON' in os.environ}")
print(f"GOOGLE_TOKEN_JSON Loaded: {'GOOGLE_TOKEN_JSON' in os.environ}")
print("----------------------------")

app = FastAPI()

class UserRequest(BaseModel):
    message: str
    session_id: str

@app.get("/")
async def root():
    return {"message": "Calendar Booking Agent is running!"}

@app.post("/chat")
async def chat(request: UserRequest):
    # This will eventually call the LangGraph agent
    inputs = {"user_prompt": request.message}
    config = {"configurable": {"thread_id": request.session_id}}
    response = agent_app.invoke(inputs, config=config)
    final_response = response.get('user_prompt') or response.get('booking_confirmation')
    return {"response": str(final_response) if final_response else "I'm sorry, I seem to have lost my train of thought. Could you please tell me what you'd like to do again?"}
