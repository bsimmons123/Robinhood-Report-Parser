import os

import pandas as pd
import datetime
from datetime import datetime


def main(chosen_file):
    # Try to load the user-provided CSV file
    try:
        df = pd.read_csv(chosen_file)
        df = df.drop(df.tail(1).index)
    except pd.errors.ParserError as e:
        print(f"A parsing error occurred: {e}")
        print("The file may contain bad or corrupt lines.")
        print(
            "If you're seeing this, sometimes Robinhood outputs data at the last line of a report which causes issues, "
            "delete that last line and then please try again.")
        exit(1)

    # prev_year = datetime.datetime.now().year - 1
    input_format = "%Y-%m-%d"

    today = pd.to_datetime('today')
    prev_year = (today - pd.DateOffset(years=1)).normalize().strftime(input_format)

    def get_validated_date(input_prompt, default_date):
        date_str = input(input_prompt)
        if not date_str:
            date_str = default_date
        if isinstance(date_str, datetime):
            return date_str
        try:
            print(date_str)
            return datetime.strptime(date_str, input_format)
        except ValueError:
            print("Invalid date format. Should be YYYY-MM-DD")
            return get_validated_date(input_prompt, default_date)

    # Loop until 'input_start_date' is a valid date
    while True:
        input_start_date = get_validated_date(
            "\nPlease enter the start date for which you would like to see all purchases (format: "
            "YYYY-MM-DD) (default: " + str(prev_year) + "): ",
            str(prev_year))
        try:
            confirm = input(f"You entered {input_start_date.strftime('%Y-%m-%d')}, is this correct? (Yes/No): ")
            if confirm.lower() == 'yes':
                break
        except ValueError:
            print(f"'{input_start_date}' is not a valid date. Please enter a valid date in the YYYY-MM-DD format.")

    # Loop until 'input_end_date' is a valid date
    while True:
        input_end_date = get_validated_date(
            "\nPlease enter the end date for which you would like to see all purchases (format: "
            "YYYY-MM-DD) (default: " + str(today.strftime('%Y-%m-%d')) + "): ",
            str(today.strftime('%Y-%m-%d')))
        try:
            confirm = input(f"You entered {input_end_date.strftime('%Y-%m-%d')}, is this correct? (Yes/No): ")
            if confirm.lower() == 'yes':
                break
        except ValueError:
            print(f"'{input_end_date}' is not a valid date. Please enter a valid date in the YYYY-MM-DD format.")

    # Convert 'input_start_date' and 'input_end_date' to datetime
    start_date = pd.to_datetime(input_start_date)
    end_date = pd.to_datetime(input_end_date)

    # Keep only rows where 'Trans Code' is 'Buy'
    df = df[df['Trans Code'] == 'Buy']

    # Convert 'Activity Date' column to date type
    df['Activity Date'] = pd.to_datetime(df['Activity Date'])

    # Filter dataframe to include only rows where 'Activity Date' is between 'prev_year_date' and 'today'
    df = df[(df['Activity Date'] >= input_start_date) & (df['Activity Date'] <= input_end_date)]

    # Convert 'Price', 'Amount and 'Quantity' column to numeric type to handle calculations
    df['Price'] = df['Price'].replace('\$', '', regex=True).replace(',', '', regex=True).astype(float)
    df['Quantity'] = df['Quantity'].astype(float)
    df['Amount'] = df['Amount'].replace('[\$,()]', '', regex=True).astype(float)

    # Calculate the total amount paid for each stock purchase
    df['Total Paid'] = df['Price'] * df['Quantity']

    # Create a 'Purchase Price' column for 'Buy' transactions based on 'Amount'
    df['Purchase Price'] = df.loc[df['Trans Code'] == 'Buy', 'Amount']

    # Filter rows where 'Activity Date' is within the range specified by user
    df = df[(df['Activity Date'] >= input_start_date) & (df['Activity Date'] <= input_end_date)]

    # Create new dataframe to store results
    result = df[['Activity Date', 'Process Date', 'Settle Date', 'Instrument', 'Description', 'Quantity', 'Price',
                 'Purchase Price']]

    result = result.sort_values(by=['Instrument'])

    pretty_date = datetime.now().strftime('%m-%d-%Y')

    csv_dir = 'output'
    csv_name = str(input_start_date.strftime('%m-%d-%Y')) + '_to_' + str(
        input_end_date.strftime('%m-%d-%Y')) + '_stocks_data_' + str(pretty_date) + '.csv'
    csv_path = os.path.join(csv_dir, csv_name)

    # Create directory if it doesn't exist
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)

    # Write output DataFrame to a CSV file
    result.to_csv(csv_path, index=False)

    print(result)

    print("\n\nStocks data has been saved to '" + csv_path + "'")
