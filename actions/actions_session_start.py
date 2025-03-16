from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType

import pandas as pd
import asyncio

class ActionSessionStart(Action):

    def name(self) -> str:
        return "action_session_start"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: dict) -> list:
        # get the call metadata from the tracker
        metadata = tracker.get_slot("session_started_metadata")
        # set appropriate slots here if that is needed usually the customer information
        
        return [] 
class ActionSleepAndRespond(Action):
    def name(self) -> str:
        return "action_sleep_few_sec"

    async def run(self, dispatcher, tracker, domain) -> list[EventType]:
        await asyncio.sleep(3)
        return []