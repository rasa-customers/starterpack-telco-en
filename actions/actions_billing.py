import pandas as pd
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class ActionVerifyBillByDate(Action):
    def name(self):
        return "action_verify_bill_by_date"

    def run(self, dispatcher, tracker, domain):
        # Load CSV file with billing data
        file_path = "bills.csv"  # Update with the correct path
        df = pd.read_csv("csvs/billing.csv")
        
        # Example CSV format:
        # customer_id,date,amount
        # 123,2025-01-01,50.00
        # 123,2025-02-01,55.00
        # 123,2025-03-01,53.00
        # 456,2025-01-15,40.00
        
        # Get customer ID and date from slots
        customer_id = tracker.get_slot("customer_id")
        bill_date = tracker.get_slot("bill_date")
        
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
                f"Your bill for {bill_date.date()} is ${bill_amount:.2f}. " + "\n"
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
        print(df)
        # Get customer_id and bill_date from slots
        customer_id = tracker.get_slot("customer_id")
        bill_date = tracker.get_slot("bill_date")
        # Convert date to datetime
        df["date"] = pd.to_datetime(df["date"])
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
            dispatcher.utter_message(f"No transactions found for customer {customer_id} on {bill_date}.")
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