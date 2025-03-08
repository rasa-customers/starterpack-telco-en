from rasa_sdk import Action
from rasa_sdk.events import EventType
from rasa_sdk.events import SlotSet
import random
import asyncio

class ActionSleepAndRespond(Action):
    def name(self) -> str:
        return "actions_run_speed_test"

    async def run(self, dispatcher, tracker, domain) -> list[EventType]:
        # dispatcher.utter_message(text="⏳")  # Send to the user

        # await asyncio.sleep(10)  # Pause for 10 seconds
        # dispatcher.utter_message(text="⌛ Almost Done ...")  # Send to the user
        
        await asyncio.sleep(10)
        dispatcher.utter_message(text="Thank you for waiting... ✅ ")  # Send to the user
        
        random_number = random.randint(50, 150)

        return [SlotSet("network_speed", random_number)]
    