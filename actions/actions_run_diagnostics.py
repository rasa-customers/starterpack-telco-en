from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import random
import asyncio

class ActionsRunSpeedTest(Action):
    def name(self) -> str:
        return "actions_run_speed_test"

    async def run(self, dispatcher, tracker, domain):
        await asyncio.sleep(10)
        # Send message to the user
        dispatcher.utter_message(text="Thank you for waiting... ✅ ")
        # We will pick randomly the internet speed here
        # * For local testing purposes you can define the number
        # * For Production testing connect to the API to get this data
        random_number = random.randint(50, 150)
        return [SlotSet("network_speed", random_number)]
