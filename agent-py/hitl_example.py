import os
from typing import Annotated, Any

from autogen import ConversableAgent, LLMConfig, register_function

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
    destination: Annotated[str, "Travel destination"],
    days: Annotated[int, "Number of days for the trip"],
    membership_type: Annotated[str, "Type of membership (premium or standard)"],
    preferences: Annotated[list, "List of traveler preferences"]
) -> dict[str, Any]:
    """Create a personalized travel itinerary based on member details"""
    
    # Create different experiences based on membership type
    if membership_type == "premium":
        accommodations = "Luxury 5-star hotel or boutique resort"
        transportation = "Private car service with dedicated driver"
        dining = "Reservations at fine dining restaurants and local gems"
        activities = f"Customized private tours focusing on {', '.join(preferences)}"
    else:
        accommodations = "Comfortable mid-range hotel"
        transportation = "Shared shuttle service and public transport options"
        dining = "Recommended local restaurants at moderate price points"
        activities = f"Group tours to popular attractions with focus on {', '.join(preferences)}"
    
    # Return the formatted itinerary
    return {
        "destination": destination,
        "days": days,
        "accommodations": accommodations,
        "transportation": transportation,
        "dining": dining,
        "activities": activities,
        "is_draft": True
    }

# Configure LLM
llm_config = LLMConfig(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
)


# Create the travel agent
with llm_config:
    travel_agent = ConversableAgent(
        name="travel_agent",
        system_message="""You are a professional travel agent who creates detailed day-by-day travel itineraries.

WORKFLOW:
1. Greet the customer warmly and ask for their member ID
2. Use the lookup_member function to retrieve their profile information
3. Address them by name and acknowledge their membership level (premium or standard)
4. Ask about their desired destination and trip duration
5. Create a personalized day-by-day itinerary using the create_itinerary function that:
    - Matches their membership level (premium: luxury options; standard: value options)
    - Incorporates their personal preferences from their profile
    - Details specific activities, meals, and accommodations for EACH day
    - Organizes attractions geographically to minimize travel time
    - Includes specific restaurant recommendations and activity timings
6. Present the complete day-by-day itinerary with clear DAY 1, DAY 2, etc. headers
7. Ask if they want any modifications to specific days
8. Confirm the final itinerary when they're satisfied

For premium members, emphasize exclusive experiences, private tours, and luxury accommodations.
For standard members, focus on good value, popular attractions, and comfortable options.

Always maintain a friendly, professional tone throughout the conversation.
""")

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
    message="Hi, I'd like to plan a vacation.",
    summary_method="reflection_with_llm"
)

response.process()
