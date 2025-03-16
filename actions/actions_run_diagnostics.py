from rasa_sdk import Action
from rasa_sdk.events import EventType
from rasa_sdk.events import SlotSet
import random
import asyncio

class ActionSleepAndRespond(Action):
    def name(self) -> str:
        return "actions_run_speed_test"

    async def run(self, dispatcher, tracker, domain) -> list[EventType]:        
        await asyncio.sleep(10)
        dispatcher.utter_message(text="Thank you for waiting... ✅ ")  # Send to the user
        
        random_number = random.randint(50, 150) # we will pick randomly the internet speed here
                                                # for local testing purposes you can define the number
                                                # for Production testing connect to the API to get this data
        return [SlotSet("network_speed", random_number)] 
    