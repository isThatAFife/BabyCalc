import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('BabyCalc')

def get_baby_data():
    """
    Get baby's data from the user.
    Run a while loop to collect a valid string of data from the user.
    Loop will repeat until valid data received (string of 2 numbers separated
    by commas).
    """
    while True:
        print("Please enter your baby's age in weeks and weight in kilograms")
        print("Data should be two numbers separated by a comma")
        print("Example: 4, 3.57\n")

        baby_str = input("Enter your data here: ")
        
        baby_data = baby_str.split(",")

        if validate_data(baby_data):
            print("Baby is valid!")
            break

    return baby_data

def validate_data(values):
    """
    Converts all string values into floats inside the try.
    Raises ValueError if strings cannot be converted into float,
    or if there aren't the correct number of values.
    """
    try:
        [float(value) for value in values]
        if len(values) != 2:
            raise ValueError(
                f"Exactly 2 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

def update_baby_worksheet(data):
    """
    Update baby worksheet, add new row with list data provided
    """
    print("Updating baby worksheet...\n")
    baby_worksheet = SHEET.worksheet("UserInput")
    baby_worksheet.append_row(data)
    print("Baby worksheet updated successfully.\n")

def calculate_formula_ml():
    print("Calculating formula...")
    result = SHEET.worksheet("UserInput").get_all_values()
    result_row = result[-1]
    print(result_row)

def main():
    """
    Run all program functions
    """
    data = get_baby_data()
    baby_data = [float(num) for num in data]
    update_baby_worksheet(baby_data)

print("Welcome to BabyCalc!\n")
main()
