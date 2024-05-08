import gspread
from tabulate import tabulate
from oauth2client.service_account import ServiceAccountCredentials



# Set up Google Sheets credentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('access.json', scope)
client = gspread.authorize(credentials)

# Open the Google Sheet
sheet = client.open('Election').sheet1

### create header if not exist
def create_headers():
    # Check if headers already exist
    headers = sheet.row_values(1)
    if "Candidate" not in headers:
        sheet.update_cell(1, 1, "Candidate")
    if "Votes" not in headers:
        sheet.update_cell(1, 2, "Votes")

def display_menu():
    print("""
    Welcome to the voting system (choice 1-5):

    1. Give vote
    2. Candidates List
    3. Add Candidate
    4. Remove Candidate
    5. Election result
    6. Exit
    """)

def give_vote():
    candidates = sheet.col_values(1)[1:]  # Get candidate names from the first column, skipping the header
    print("Candidates:")
    for i, candidate in enumerate(candidates, 1):
        print(f"{i}. {candidate}")

    choice = int(input("Enter the number of the candidate you want to vote for: "))
    if 1 <= choice <= len(candidates):
        cell = sheet.find(candidates[choice-1])
        sheet.update_cell(cell.row, 2, int(sheet.cell(cell.row, 2).value) + 1)
        print("Vote successfully casted.")
    else:
        print("Invalid choice.")
    return True

def candidates_list():
    candidates = sheet.col_values(1)[1:]  # Get candidate names from the first column, skipping the header
    print("Candidates:")
    for i, candidate in enumerate(candidates, 1):
        print(f"{i}. {candidate}")
    return True


def add_candidate():
    candidate_name = input("Enter the name of the candidate you want to add: ")
    sheet.append_row([candidate_name, 0])
    print("Candidate added successfully.")
    return True

def remove_candidate():
    candidate_name = input("Enter the name of the candidate you want to remove: ")
    candidates = sheet.col_values(1)[1:]  # Get candidate names from the first column, skipping the header
    if candidate_name in candidates:
        cell = sheet.find(candidate_name)
        sheet.delete_row(cell.row)
        print("Candidate removed successfully.")
    else:
        print("Candidate not found.")
    return True

def election_result():
    candidates = sheet.col_values(1)[1:]  # Get candidate names from the first column, skipping the header
    result_table = []
    for candidate in candidates:
        cell = sheet.find(candidate)
        votes = int(sheet.cell(cell.row, 2).value)
        result_table.append([candidate, votes])

    print("Election Result:")
    print(tabulate(result_table, headers=['Candidates', 'Votes'], tablefmt='grid'))
    return True

# Main function
def main():
    create_headers()  # Create headers if they don't exist
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ")
        if choice == '1':
            give_vote()
        elif choice == '2':
            candidates_list()
        elif choice == '3':
            add_candidate()
        elif choice == '4':
            remove_candidate()
        elif choice == '5':
            election_result()
        elif choice == '6':
            break  # Exit the loop
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
        
        # Prompt for Enter to continue or F to exit
        choice = input("Press Enter to continue or 'F' to exit: ")
        if choice.upper() == 'F':
            break

if __name__ == "__main__":
    main()
