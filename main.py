from datetime import datetime

import pandas as pd
import yearly_report_ind
import yearly_report_full
import os
import glob

# Get the current working directory
curr_dir = os.getcwd()

# Use glob to match .csv file pattern
csv_files = glob.glob(os.path.join(curr_dir, '*.csv'))

# Print the list of .csv files
print("List of CSV files:")
for i, file in enumerate(csv_files):
    print(f"{i + 1}. {os.path.basename(file)}")

# Input loop
while True:
    choice = input("\nEnter the number of the file you want to use, or type 'quit' to exit: ")

    if choice.lower() == 'quit':
        print("User chose to quit.")
        exit(1)
    elif choice.isdigit():
        chosen_file_index = int(choice) - 1
        if 0 <= chosen_file_index < len(csv_files):
            chosen_file = csv_files[chosen_file_index]
            print(f"\nYou chose the file: {os.path.basename(chosen_file)}")
            break
        else:
            print("Invalid file number. Please try again.")
    else:
        print("Invalid input. Please enter a file number or 'quit'.")

# Ask user what they want to do
action = input("What do you want to do? \n1. Run a yearly report \n2. Run a full average report \n3. Run an individual average report\nEnter 1, 2, or 3: ")

if action == '1':
    # Call the yearly report script
    yearly_report_ind.main(chosen_file=chosen_file)

elif action == '2':
    # Call the yearly report script
    yearly_report_full.main(chosen_file=chosen_file)

elif action == '3':
    # Ask the user for the filename
    file_name = chosen_file

    # Try to load the user-provided CSV file
    try:
        df = pd.read_csv(file_name)
        df = df.head(-1)
    except pd.errors.ParserError as e:
        print(f"A parsing error occurred: {e}")
        print("The file may contain bad or corrupt lines.")
        exit(1)

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
    csv_name = 'ind_average_stocks_data_' + str(pretty_date) + '.csv'
    csv_path = os.path.join(csv_dir, csv_name)

    # Create directory if it doesn't exist
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)

    # Write output DataFrame to a CSV file
    result.to_csv(csv_path, index=False)

    print("\n\nStocks data has been saved to '" + csv_path + "'")


else:
    print("Invalid choice. Please enter 1 to run a yearly report, or 2 to run an average report.")
