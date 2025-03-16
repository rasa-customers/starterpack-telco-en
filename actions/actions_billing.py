import pandas as pd
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from datetime import datetime
import logging

class ActionVerifyBillByDate(Action):
    def name(self):
        return "action_verify_bill_by_date"
    def text_to_date(month_text):
        try:
            # Get the current year
            current_year = datetime.now().year
            
            # Combine user input with the current year
            full_text = f"{month_text} {current_year}"
            
            # Parse the text format (e.g., "March 2025")
            date_obj = datetime.strptime(full_text, "%B %Y")
            
            # Format as DD/MM/YYYY (defaults to the first day of the month)
            formatted_date = date_obj.strftime("01/%m/%Y")
            logging.info(f"This is an info message: formatted_date: {formatted_date}")
            return formatted_date
        except ValueError:
            return "Invalid format. Please use a full month name (e.g., 'March')."
    
    def run(self, dispatcher, tracker, domain):
        # Load CSV file with billing data
        file_path = "bills.csv"  # Update with the correct path
        df = pd.read_csv("csvs/billing.csv")

        # Get customer ID and date from slots
        customer_id = tracker.get_slot("customer_id")
        bill_month = tracker.get_slot("bill_month")
        #logging.info(f"This is an info message: bill_month : {bill_month}")

        bill_date = ActionVerifyBillByDate.text_to_date(bill_month)
        #logging.info(f"This is an info message: bill_month after transformation: {bill_date}")
        
        if not customer_id:
            dispatcher.utter_message("I couldn't find your customer ID. Please provide it.")
            return []
        
        if not bill_date:
            dispatcher.utter_message("Please specify the date for the bill you want to check.")
            return []
        
        # Convert date to datetime
        df["date"] = pd.to_datetime(df["date"])
        bill_date = pd.to_datetime(bill_date)
    
        # Filter data for the given customer and date
        customer_bills = df[df["customer_id"] == int(customer_id)]
        specific_bill = customer_bills[customer_bills["date"] == bill_date]
        
        if specific_bill.empty:
            dispatcher.utter_message(f"No bill found for {bill_date.date()}.")
            return []
        
        bill_amount = specific_bill.iloc[0]["amount"]
        average_bill = customer_bills["amount"].mean()
        difference = bill_amount - average_bill
        
        # Generate response
        response = (
                f"Your bill for {bill_month} {bill_date.date().year} is ${bill_amount:.2f}. " + "\n"
                f"The average of your past bills is ${average_bill:.2f}. " + "\n"
                f"This bill is {'higher' if difference > 0 else 'lower'} than your average by ${abs(difference):.2f}.")
        
        dispatcher.utter_message(response)
        return [SlotSet("bill_amount", int(bill_amount)),
                SlotSet("average_bill", int(average_bill)),
                SlotSet("difference", int(difference))]


class ActionRecapBill(Action):
    def name(self):
        return "action_recap_bill"

    def run(self, dispatcher, tracker, domain):
        # Path to the CSV file (Update path if necessary)
        csv_path = "csvs/billing.csv"  
        
        # Read the CSV
        df = pd.read_csv(csv_path)
        print(df) # this can be shown in the logs of your custom action, if you want the message to be displayed to the user use 'dispatcher.utter_message'
        # Get customer_id and bill_date from slots
        customer_id = tracker.get_slot("customer_id")
        bill_month = tracker.get_slot("bill_month")
        # Convert date to datetime
        df["date"] = pd.to_datetime(df["date"])
        bill_date = ActionVerifyBillByDate.text_to_date(bill_month)
        bill_date = pd.to_datetime(bill_date)

        if not customer_id:
            dispatcher.utter_message("I need your customer ID to fetch your bill recap.")
            return []
        
        if not bill_date:
            dispatcher.utter_message("I need a date to fetch your bill recap. Can you provide one?")
            return []

        # Convert customer_id to int if needed
        try:
            customer_id = int(customer_id)
        except ValueError:
            dispatcher.utter_message("Invalid customer ID format.")
            return []

        # Filter records for the given customer_id and date
        filtered_df = df[(df["customer_id"] == customer_id)]

        if filtered_df.empty:
            dispatcher.utter_message(f"No transactions found for customer {customer_id} on {bill_date_text}.")
            return []

        # Format the output
        response1= (
            "Here is a summary of your costs :"
            )
        dispatcher.utter_message(response1)
        response = ( 
            f"\n".join([f"{row['date'].date()} | {row['amount']} $ | {row['source']}" for _, row in filtered_df.iterrows()])
        )
        # Send response to user
        dispatcher.utter_message(response)
        print("response heeere", response)
        return []