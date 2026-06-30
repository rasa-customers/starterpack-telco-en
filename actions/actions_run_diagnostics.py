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
        # We pick the internet speed randomly here.
        # * For Production, connect to the API to get this data.
        # * For deterministic e2e tests, set the `network_speed_override` slot via a
        #   fixture and we use that instead of a random value (see
        #   tests/e2e_test_cases/internet_slow_test_case.yml). It is unset in
        #   production, so behaviour there is unchanged.
        override = tracker.get_slot("network_speed_override")
        speed = int(override) if override is not None else random.randint(10, 140)
        return [SlotSet("network_speed", speed)]
