from rasa_sdk import Action, Tracker
import asyncio

class ActionSessionStart(Action):
    def name(self) -> str:
        return "action_session_start"

    def run(self, dispatcher, tracker, domain):
        # Get the call metadata from the tracker
        # * Use metadata to set customer information slots if needed
        #metadata = tracker.get_slot("session_started_metadata")
        return []


class ActionSleepAndRespond(Action):
    def name(self) -> str:
        return "action_sleep_few_sec"

    async def run(self, dispatcher, tracker, domain):
        await asyncio.sleep(3)
        return []