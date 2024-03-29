# Robinhood Report Parser

Robinhood Report Parser is a Python script designed to parse, summarize, and analyze financial report data from the Robinhood trading platform.

# Why it's needed
When I migrated Broker accounts, Robinhood did not include any trading details from my stock purchases so I had to generate a report of all of my stocks and parse out when I bought each stock and for how much money I paid for each stock. I had to generate a list of every stock i've purchased in the last year and at what price i bought the stocks at. I then also generated an average price paid for every stock that I own. This was the only solution I could think of that didn't involve me sitting with a pen and paper generating this data to input into my new brokerage.  

## Overview

There are several Python files in this project each with their specific functionalities:

1. `main.py` - Intended to be the **main** entry point for the application. It allows the user to select a CSV file to parse and summarizes the data including total quantities, total paid, average prices, total value, and the last purchase dates.

2. `yearly_report_full.py` - This script allows the user to provide a date range, and then it will analyze all of the stock purchases made during that period. It starts by loading a provided CSV file and parses the data, removing any potentially corrupt lines that might arise from the last line of a Robinhood report.

    The script then prompts for a start and end date Enter dates in the YYYY-MM-DD format, which are used to filter the data for the period of interest. The script then filters the data further to consider only 'Buy' transactions.

    The data is then grouped together by the 'Instrument' (presumably the ticker Symbol for the stocks), and various calculations are performed such as total amount paid for each stock, total quantity per stock, average price per instrument, total value of each stock, and the latest purchase date for each stock.

    The results are then printed in the console and saved to a CSV file in an `output` directory, with the filename including the date range and current date.
3. `yearly_report_ind.py` - This script functions similarly to `yearly_report_full.py` and parses Robinhood data for a given user-defined date range. After loading the data and cleaning it (e.g., removing potential corrupt lines from the end of the report, focusing only on 'Buy' transactions), the script asks for input from the console for a start and an end date for the range of interest.

    Unlike `yearly_report_full.py`, this script does not group data by the instrument, but maintains the data on a purchase-by-purchase basis, based on the 'Activity Date' column. Therefore, this script may be more helpful for those who want a detailed, transaction-by-transaction analysis of their Robinhood data within the defined date range, while 'yearly_report_full.py' may be for those who want a more high-level summary.

    The data is then separated into a DataFrame concentrating on details such as the 'Activity Date', 'Process Date', 'Settle Date', 'Instrument', 'Description', 'Quantity', 'Price', and 'Purchase Price'. These results are then printed to the console and logged in a CSV file.
These scripts provide comprehensive parsing and analysis of Robinhood financial data to help users understand their financial report.

## Getting Started

### Prerequisites

- Python 3.10.0
- Required Packages: numpy, pandas, pip, pyarrow, python-dateutil, pytz, setuptools, six, tzdata, wheel.

### Installation

1. Clone this repository to your local machine.

    ```bash
    git clone https://github.com/bsimmons123/Robinhood-Report-Parser
    cd Robinhood-Report-Parser
    ```

2. Install all required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Place your [generated report](https://robinhood.com/account/reports-statements/activity-reports) in the base of the project.

2. Run the `main.py` script in the command line with the following format:

    ```bash
    python main.py
    ```

3. Select a CSV file to parse and follow the prompts.

Output should look similar to this:
```shell
main.py robinhood-report.csv 
List of CSV files:
1. robinhood-report.csv

Enter the number of the file you want to use, or type 'quit' to exit: 1

You chose the file: robinhood-report.csv
What do you want to do? 
1. Run a yearly report 
2. Run a full average report 
3. Run an individual average report
Enter 1, 2, or 3: 
```