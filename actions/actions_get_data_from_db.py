from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import pandas as pd

class ActionGetCustomerInfo(Action):
    def name(self):
        return "action_get_customer_info"

    def run(self, dispatcher, tracker, domain):
        #Load CSV file
        file_path = "csvs/customers.csv"  # get information from your DBs
        df = pd.read_csv(file_path)
        customer_id = tracker.get_slot("customer_id")

        # Filter data for the given customer ID
        customer_info = df[df["customer_id"] == int(customer_id)]

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
        return [ SlotSet("customer_first_name", first_name)]
