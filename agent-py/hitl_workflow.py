import os
from typing import Annotated, Any

from autogen import ConversableAgent, LLMConfig, register_function

from fastapi import FastAPI

from fastagency import UI
from fastagency.adapters.awp import AWPAdapter
from fastagency.runtimes.ag2 import Workflow

# Mock user database
MEMBER_DATABASE = {
    "P12345": {
        "name": "Alex Johnson",
        "membership": "premium",
        "preferences": [
            "5-star hotels",
            "fine dining",
            "private tours",
            "exclusive experiences",
        ],
    },
    "P67890": {
        "name": "Taylor Williams",
        "membership": "premium",
        "preferences": [
            "boutique hotels",
            "local cuisine",
            "cultural experiences",
            "adventure activities",
        ],
    },
    "S12345": {
        "name": "Jordan Smith",
        "membership": "standard",
        "preferences": ["budget-friendly", "popular attractions"],
    },
    "S67890": {
        "name": "Casey Brown",
        "membership": "standard",
        "preferences": ["family-friendly", "group tours"],
    },
}

# Travel agent function to look up member information
def lookup_member(
    member_id: Annotated[str, "User's membership ID"]
) -> dict[str, Any]:
    """Look up member details from the database"""
    if member_id in MEMBER_DATABASE:
        return {
            "found": True,
            "name": MEMBER_DATABASE[member_id]["name"],
            "membership": MEMBER_DATABASE[member_id]["membership"],
            "preferences": MEMBER_DATABASE[member_id]["preferences"]
        }
    else:
        return {
            "found": False,
            "message": "Member ID not found in our system"
        }

# Function to create personalized itinerary
def create_itinerary(
    destination: Annotated[str, "Travel destination (e.g., New York, Paris, Tokyo)"],
    days: Annotated[int, "Number of days for the trip"],
    membership_type: Annotated[str, "Type of membership (premium or standard)"],
    preferences: Annotated[list, "Traveler preferences (e.g., fine dining, cultural tours)"]
) -> dict[str, Any]:
    """Create a realistic, personalized travel itinerary based on member details."""
    
    if not destination or days <= 0:
        return {"error": "Invalid destination or number of days."}

    itinerary = []
    for day in range(1, days + 1):
        day_plan = {
            "day": f"Day {day}",
            "morning": "",
            "afternoon": "",
            "evening": "",
        }

        if membership_type == "premium":
            day_plan["morning"] = f"Private tour or exclusive experience aligned with: {', '.join(preferences)}"
            day_plan["afternoon"] = "Relax at a luxury spa, explore high-end shopping districts, or enjoy curated local experiences."
            day_plan["evening"] = "Dine at a top-rated restaurant with a reservation made just for you."
        else:
            day_plan["morning"] = f"Join a small group tour covering key attractions related to: {', '.join(preferences)}"
            day_plan["afternoon"] = "Take a self-guided walk or visit a popular local spot recommended by travel experts."
            day_plan["evening"] = "Enjoy a casual dinner at a popular neighborhood restaurant."

        itinerary.append(day_plan)

    return {
        "destination": destination,
        "days": days,
        "itinerary": itinerary,
        "accommodation": "5-star hotel" if membership_type == "premium" else "3-star or boutique hotel",
        "transportation": "Private car service" if membership_type == "premium" else "Local transport and shared rides",
        "is_draft": True
    }

# Configure LLM
llm_config = LLMConfig(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
)

wf = Workflow()

SYSTEM_MESSAGE="""You are a professional travel agent who creates detailed, personalized day-by-day travel itineraries for any destination.

WORKFLOW:
1. Greet the customer warmly and ask for their member ID.
2. Use the `lookup_member` function to retrieve their profile information.
3. Address the customer by name and acknowledge their membership level (premium or standard).
4. Ask for their desired destination, specific cities (if applicable), travel start date, and trip duration.
    - If the customer mentions only a country (e.g., "USA" or "Croatia"), ask them which cities they'd like to visit.
    - If they're unsure, suggest 2–3 well-known cities in that country based on general travel knowledge.
5. Use the `create_itinerary` function to generate a personalized day-by-day itinerary that:
    - Aligns with their membership level (e.g., premium → luxury hotels, fine dining; standard → comfort & value).
    - Includes named **hotels, restaurants, attractions, and activities** based on typical travel knowledge for the selected cities.
    - Provides **specific daily structure**: morning, afternoon, evening.
    - Minimizes travel time by grouping activities geographically.
    - Feels locally authentic and realistic even though this is a demo (do not say “sample” or “example” in the response).
    - If the user provides no preferences, generate a balanced mix of culture, food, leisure, and exploration.
6. Present the itinerary with clear headers (e.g., **Day 1**, **Day 2**), using markdown-style formatting if supported.
7. Ask if the customer would like to modify any days, switch cities, or add/remove experiences.
8. Once finalized, confirm the itinerary and thank them for using the service.

Tone: Friendly, professional, and knowledgeable. You are a helpful concierge who wants the user to have an amazing experience.

Important: When a membership ID is not found in the system, politely inform the user that something may be wrong and ask them to double-check their ID."""



INITIAL_MESSAGE = """Hi there! 👋 I'm your personal Travel Guide, here to help you plan an unforgettable trip.

To get started, could you please share your membership ID? This will help me tailor recommendations based on your preferences and travel style.

(Hint: You can try using one of these IDs: P12345, P67890, S12345, S67890. And when the agent is asking your permission to execute the function, please say "continue" to proceed.)
"""

@wf.register(name="hitl_workflow", description="A simple travel itenarary generator workflow")
def hitl_workflow(ui: UI, params: dict[str, Any]) -> str:
    initial_message = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt=INITIAL_MESSAGE,
    )
    
    # Create the travel agent
    with llm_config:
        travel_agent = ConversableAgent(
                name="travel_agent",
                system_message=SYSTEM_MESSAGE
            )
        

    # Create the customer agent (human input)
    customer = ConversableAgent(
        name="customer",
        human_input_mode="ALWAYS",  # Always ask for human input
    )

    # Register the functions for the travel agent
    register_function(
        lookup_member,
        caller=travel_agent,
        executor=customer,
        description="Look up member details from the database"
    )

    register_function(
        create_itinerary,
        caller=travel_agent,
        executor=customer,
        description="Create a personalized travel itinerary based on member details"
    )

    # Start the conversation
    response = customer.run(
        travel_agent,
        message=initial_message,
        summary_method="reflection_with_llm"
    )

    return ui.process(response)  # type: ignore[no-any-return]


def without_customer_messages(message: Any) -> bool:
    return not (message.type == "text" and message.content.sender == "customer")


adapter = AWPAdapter(
    provider=wf, wf_name="hitl_workflow", filter=without_customer_messages
)

app = FastAPI()
app.include_router(adapter.router)


# start the provider with the following command
# uvicorn hitl_workflow:app --port 8008 --reload
