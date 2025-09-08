from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet

import random
import asyncio

class ActionsRunSpeedTest(Action):
    def name(self) -> str:
        return "actions_run_speed_test"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> List[Dict[Text, Any]]:
        await asyncio.sleep(10)
        # Send message to the user
        dispatcher.utter_message(text="Thank you for waiting... ✅ ")
        # We will pick randomly the internet speed here
        # * For local testing purposes you can define the number
        # * For Production testing connect to the API to get this data
        random_number = random.randint(10, 140)
        return [SlotSet("network_speed", random_number)]
