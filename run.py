import gspread
from google.oauth2.service_account import Credentials

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
    Get baby's data from the user
    """
    print("Please enter your baby's age in weeks and weight in kilograms")
    print("Data should be two numbers separated by a comma")
    print("Example: 4, 3.57\n")

    baby_str = input("Enter your data here:")
    
    baby_data = baby_str.split(",")
    validate_data(baby_data)

def validate_data(values):
    try:
        if len(values) != 2:
            raise ValueError(
                f"Exactly 2 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")

get_baby_data()
