from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet

import pandas as pd

class ActionGetCustomerInfo(Action):
    def name(self):
        return "action_get_customer_info"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> List[Dict[Text, Any]]:
        #Load CSV file
        file_path = "csvs/customers.csv"  # get information from your DBs
        df = pd.read_csv(file_path)
        customer_id = tracker.get_slot("customer_id")

        # Check if customer_id exists and is valid
        if customer_id is None:
            dispatcher.utter_message("Customer ID not provided.")
            return []
        try:
            customer_id_int = int(customer_id)
        except (ValueError, TypeError):
            dispatcher.utter_message("Invalid customer ID format.")
            return []

        # Filter data for the given customer ID
        customer_info = df[df["customer_id"] == customer_id_int]

        if customer_info.empty:
            dispatcher.utter_message("No customer found with this ID.")
            return []

        # Extract customer details
        first_name = customer_info.iloc[0]["first_name"]
        last_name = customer_info.iloc[0]["last_name"]

        # Generate response
        response = (f"Customer Details:\n"
                    f"First Name: {first_name}\n"
                    f"Last Name: {last_name}\n")
        #dispatcher.utter_message(response)

        # Set the retrieved name in a slot
        return [SlotSet("customer_first_name", first_name)]
