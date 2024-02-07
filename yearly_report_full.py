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

    df['Activity Date'] = pd.to_datetime(df['Activity Date'])

    df = df[(df['Activity Date'] >= input_start_date) & (df['Activity Date'] <= input_end_date)]

    # Keep only rows where 'Trans Code' is 'Buy'
    df = df[df['Trans Code'] == 'Buy']

    # Convert 'Activity Date' column to date type
    df['Activity Date'] = pd.to_datetime(df['Activity Date'])

    # Convert 'Price' and 'Quantity' column to numeric type to handle calculations
    price = df['Price'].replace('\$', '', regex=True).replace(',', '', regex=True)
    df['Price'] = pd.to_numeric(price)
    df['Quantity'] = pd.to_numeric(df['Quantity'])

    # Calculate the total amount paid for each stock purchase
    df['Total Paid'] = df['Price'] * df['Quantity']

    # Group the data by 'Instrument'
    grouped_data = df.groupby('Instrument')

    # Calculate total amount paid for each stock
    total_paid = grouped_data['Total Paid'].sum()

    # Calculate total quantity for each stock
    total_quantity = grouped_data['Quantity'].sum()

    # Compute average price per instrument
    average_prices = total_paid / total_quantity

    # Calculate total value of each stock
    total_value = total_quantity * average_prices

    # Get the latest purchase date for each stock
    last_purchase_dates = grouped_data['Activity Date'].max()

    # Create a new DataFrame to hold the average prices, last purchase dates and total values
    # The instruments themselves become the index of the DataFrame
    data = pd.DataFrame({
        'Average Price': average_prices,
        'Last Purchase Date': last_purchase_dates,
        'Quantity': total_quantity,
        'Total Value': total_value
    })

    data.reset_index(level=0, inplace=True)

    # Convert the dictionary with data into a DataFrame
    result = pd.DataFrame(data)

    # Print the result
    print(result)

    pretty_date = datetime.now().strftime('%m-%d-%Y')

    csv_dir = 'output'
    csv_name = 'full_average_stocks_data_' + str(input_start_date.strftime('%m-%d-%Y')) + '_to_' + str(
        input_end_date.strftime('%m-%d-%Y')) + '_stocks_data_' + str(pretty_date) + '.csv'
    csv_path = os.path.join(csv_dir, csv_name)

    # Create directory if it doesn't exist
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)

    # Write output DataFrame to a CSV file
    result.to_csv(csv_path, index=False)

    print("\n\nStocks data has been saved to '" + csv_path + "'")
