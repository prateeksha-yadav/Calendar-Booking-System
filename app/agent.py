from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv
from app.tools.google_calendar import get_available_slots, book_appointment
import datetime
from langgraph.checkpoint.memory import MemorySaver

# load_dotenv() # This line is only for local development

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY not found in the .env file. "
        "Please create a .env file in the project root and add your key, e.g., GOOGLE_API_KEY='...'"
    )

class AgentState(BaseModel):
    user_prompt: str = Field(default="")
    available_slots: list = Field(default_factory=list)
    selected_slot: str = ""
    booking_confirmation: str = ""
    date: str = ""


# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)

def get_user_intent(state: AgentState):
    prompt = f"""
    Analyze the user prompt to determine the desired date for an appointment.
    Today's date is {datetime.date.today()}.
    User prompt: '{state.user_prompt}'
    Return a JSON object with a single key "date" and the value as the extracted date in "YYYY-MM-DD" format.
    If no specific date is found, return an empty JSON object.
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    try:
        import json
        clean_response = response.content.strip().replace("```json", "").replace("```", "")
        intent = json.loads(clean_response)
        if "date" in intent and intent.get("date"):
            intent["date"] = intent["date"].split("T")[0]
        return intent
    except (json.JSONDecodeError, AttributeError):
        return {}

def check_availability(state: AgentState):
    intent_result = get_user_intent(state)
    date = intent_result.get("date")
    if date:
        try:
            slots = get_available_slots(date)
            if slots:
                slots_str = ", ".join([datetime.datetime.fromisoformat(s).strftime('%I:%M %p') for s in slots])
                response_msg = f"I have the following slots available: {slots_str}. Which one would you like to book?"
                return {"date": date, "available_slots": slots, "user_prompt": response_msg}
            else:
                response_msg = f"I'm sorry, I don't have any available slots on {date}. Would you like to try another date?"
                return {"date": "", "available_slots": [], "user_prompt": response_msg}
        except Exception as e:
            return {"date": "", "available_slots": [], "user_prompt": f"I encountered an error while checking my calendar: {e}. Please try again."}
    return {"date": "", "available_slots": [], "user_prompt": "I'm not sure what date you'd like to book. Please specify a date like 'tomorrow' or 'this Friday'."}

def confirm_booking(state: AgentState):
    # Create a numbered list of slots for the LLM to understand context
    slot_options = "\n".join([f"{i+1}. {datetime.datetime.fromisoformat(s).strftime('%I:%M %p')}" for i, s in enumerate(state.available_slots)])

    selection_prompt = f"""
    A user is choosing from a list of available appointment times.
    
    Here are the available slots for {state.date}:
    {slot_options}
    
    The user's response was: "{state.user_prompt}"
    
    Based on their response, which slot number did they pick? 
    You MUST return a JSON object with a single key "slot_number" and the value as the integer number they chose.
    
    For example:
    - If the user says "I'll take the second one", you return {{"slot_number": 2}}
    - If the user says "9 AM please", and that is option 1, you return {{"slot_number": 1}}
    - If the user says "The 4pm slot works", and that is option 8, you return {{"slot_number": 8}}
    
    If you cannot determine which number they chose, return {{"slot_number": null}}.
    """
    response = llm.invoke([HumanMessage(content=selection_prompt)])
    try:
        import json
        clean_response = response.content.strip().replace("```json", "").replace("```", "")
        result = json.loads(clean_response)
        slot_number = result.get("slot_number")

        if slot_number is not None and 1 <= slot_number <= len(state.available_slots):
            # The slot number is 1-based, so subtract 1 for the list index
            selected_slot = state.available_slots[slot_number - 1]
            
            confirmation_link = book_appointment(selected_slot, summary="Meeting booked via AI Assistant")
            user_email = "prateekshayadav01102004@gmail.com"
            confirmation_message = (
                f"Success! The appointment has been booked on your Google Calendar ({user_email}).\n\n"
                f"You can view the new event here: {confirmation_link}"
            )
            return {"booking_confirmation": confirmation_message}
        else:
            return {"user_prompt": "I didn't quite understand which time you'd like. Please pick one from the list I provided."}

    except (json.JSONDecodeError, AttributeError, TypeError):
        return {"user_prompt": "I'm having trouble understanding. Could you please specify one of the times I suggested?"}


def entry_router(state: AgentState):
    if not state.available_slots:
        return "check_availability"

    router_prompt = f"""
    You are an AI assistant helping a user book an appointment.
    The user was just shown a list of available time slots.
    The user's latest message is: "{state.user_prompt}"

    Based on this message, are they trying to select a time or are they asking a new question?
    Choose one: "confirm_booking" or "check_availability"
    Return a single JSON object with the key "action" and your choice as the value.
    """
    response = llm.invoke([HumanMessage(content=router_prompt)])
    try:
        import json
        decision = json.loads(response.content.strip().replace("```json", "").replace("```", ""))
        return decision.get("action", "check_availability")
    except Exception:
        return "check_availability"

def start_node(state):
    return {}

# Define the graph
workflow = StateGraph(AgentState)
workflow.add_node("start", start_node)
workflow.add_node("check_availability", check_availability)
workflow.add_node("confirm_booking", confirm_booking)
workflow.set_entry_point("start")

workflow.add_conditional_edges(
    "start",
    entry_router,
    {
        "check_availability": "check_availability",
        "confirm_booking": "confirm_booking",
    },
)

# Compile the graph with memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)