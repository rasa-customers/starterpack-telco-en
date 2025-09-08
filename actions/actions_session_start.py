from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

import asyncio

class ActionSessionStart(Action):
    def name(self) -> str:
        return "action_session_start"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> List[Dict[Text, Any]]:
        # Get the call metadata from the tracker
        # * Use metadata to set customer information slots if needed
        #metadata = tracker.get_slot("session_started_metadata")
        return []


class ActionSleepAndRespond(Action):
    def name(self) -> str:
        return "action_sleep_few_sec"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> List[Dict[Text, Any]]:
        await asyncio.sleep(3)
        return []