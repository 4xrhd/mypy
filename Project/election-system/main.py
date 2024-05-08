import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up Google Sheets credentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('access.json', scope)
client = gspread.authorize(credentials)

# Open the Google Sheet
sheet = client.open('Election').sheet1

def display_menu():
    print("""
    Welcome to the voting system (choice 1-5):

    1. Give vote
    2. Candidates List
    3. Add Candidate
    4. Remove Candidate
    5. Election result
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

def candidates_list():
    candidates = sheet.col_values(1)[1:]  # Get candidate names from the first column, skipping the header
    print("Candidates:")
    for candidate in candidates:
        print(candidate)

def add_candidate():
    candidate_name = input("Enter the name of the candidate you want to add: ")
    sheet.append_row([candidate_name, 0])
    print("Candidate added successfully.")

def remove_candidate():
    candidate_name = input("Enter the name of the candidate you want to remove: ")
    candidates = sheet.col_values(1)[1:]  # Get candidate names from the first column, skipping the header
    if candidate_name in candidates:
        cell = sheet.find(candidate_name)
        sheet.delete_row(cell.row)
        print("Candidate removed successfully.")
    else:
        print("Candidate not found.")

def election_result():
    candidates = sheet.col_values(1)[1:]  # Get candidate names from the first column, skipping the header
    print("Election Result:")
    for candidate in candidates:
        cell = sheet.find(candidate)
        votes = int(sheet.cell(cell.row, 2).value)
        print(f"{candidate}: {votes} votes")

# Main function
def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")
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
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()

