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
    print(f"The data provided is {baby_str}")

get_baby_data()