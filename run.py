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
    Get baby's data from the user.
    Run a while loop to collect a valid string of data from the user.
    Loop will repeat until valid data received (string of 2 numbers separated
    by commas).
    """
    while True:
        print("Please enter your baby's age in weeks and weight in kilograms")
        print("Data should be two numbers separated by a comma")
        print("Example: 4, 3.57\n")

        baby_str = input("Enter your data here:\n")

        baby_data = baby_str.split(",")

        if validate_data(baby_data):
            print("Data is valid!\n")
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
    Update baby worksheet, add new row with list data provided.
    Also, calculate and return the change in age and weight since the previous entry.

    Args:
        data (list): A list containing the baby's age in weeks and weight in kilograms.

    Returns:
        tuple: A tuple containing the change in age (in weeks) and weight (in kilograms) since the previous entry.
    """
    print("Updating baby worksheet...\n")
    baby_worksheet = SHEET.worksheet("UserInput")

    # Get the previous entry, if any
    previous_data = baby_worksheet.get_all_values()
    if len(previous_data) > 0:
        # Check if the previous data row is valid
        if all(x.strip() for x in previous_data[-1]):
            previous_age_weeks, previous_weight_kg = [
                float(x) for x in previous_data[-1]]
        else:
            previous_age_weeks, previous_weight_kg = 0, 0
    else:
        previous_age_weeks, previous_weight_kg = 0, 0

    # Calculate the change in age and weight
    age_change_weeks = data[0] - previous_age_weeks
    weight_change_kg = data[1] - previous_weight_kg

    # Append the new data to the worksheet
    baby_worksheet.append_row(data)

    print("Baby worksheet updated successfully.\n")
    return age_change_weeks, weight_change_kg


def calculate_formula_amount(age_weeks, weight_kg):
    """
    Calculates the amount of formula (in milliliters) a baby needs per day
    based on their age in weeks and weight in kilograms.

    Args:
        age_weeks (float): The baby's age in weeks.
        weight_kg (float): The baby's weight in kilograms.

    Returns:
        float: The amount of formula (in milliliters) the baby needs per day.
    """
    if age_weeks < 2:
        formula_ml_per_kg_per_day = 150
    elif age_weeks < 6:
        formula_ml_per_kg_per_day = 120
    elif age_weeks < 12:
        formula_ml_per_kg_per_day = 110
    else:
        formula_ml_per_kg_per_day = 100

    formula_amount_ml_per_day = formula_ml_per_kg_per_day * weight_kg
    return formula_amount_ml_per_day


def main():
    """
    Run all program functions
    """
    data = get_baby_data()
    baby_data = [float(num) for num in data]
    age_weeks, weight_kg = baby_data

   # Calculate the formula amount
    formula_amount_ml = calculate_formula_amount(age_weeks, weight_kg)
    print(f"Your baby needs {formula_amount_ml:.2f} millilitres of formula per day\n")

    # Update the spreadsheet and get the change in age and weight
    age_change_weeks, weight_change_kg = update_baby_worksheet(baby_data)
    print(f"Since the last entry, your baby's age has changed by {age_change_weeks:.2f} weeks and their weight has changed by {weight_change_kg:.2f} kilograms.\n")
    print("Thank you for using BabyCalc!")


banner = """ 
______       _           _____       _      
| ___ \\     | |         /  __ \\     | |     
| |_/ / __ _| |__  _   _| /  \\/ __ _| | ___ 
| ___ \\/ _` | '_ \\| | | | |    / _` | |/ __|
| |_/ / (_| | |_) | |_| | \\__/\\ (_| | | (__ 
\\____/ \\__,_|_.__/ \\__, |\\____/\\__,_|_|\\___|
                    __/ |                   
                   |___/                    
"""
print(banner)
print("Welcome to BabyCalc!\n")
main()
