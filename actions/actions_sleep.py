from rasa_sdk import Action
from rasa_sdk.events import EventType
import time

class ActionSleepAndRespond(Action):
    def name(self) -> str:
        return "action_sleep_and_respond"

    def run(self, dispatcher, tracker, domain) -> list[EventType]:
        dispatcher.utter_message(text="Perfect! 10 seconds has passed .. ⌛ ..")  # Send to the user
        time.sleep(10)  # Pause for 10 seconds

        return []