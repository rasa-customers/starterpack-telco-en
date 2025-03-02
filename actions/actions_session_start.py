import os
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from twilio.rest import Client

class ActionSessionStart(Action):

    def name(self) -> str:
        return "action_session_start"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: dict) -> list:
        # get the call metadata from the tracker
        metadata = tracker.get_slot("session_started_metadata")
        # set appropriate slots
        if metadata:
            return [
                SlotSet("user_name", metadata.get("user_phone")),
            ]

        return []