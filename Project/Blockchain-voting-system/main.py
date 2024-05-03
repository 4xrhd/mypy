import gspread
from oauth2client.service_account import ServiceAccountCredentials
import hashlib
import json
import time

# Connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Open the Google Sheets document
sheet = client.open("Blockchain Voting System").sheet1

# Function to calculate hash of a block
def calculate_hash(block):
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

# Function to create a new block
def create_block(vote, previous_hash):
    block = {
        'index': len(blockchain) + 1,
        'timestamp': time.time(),
        'vote': vote,
        'previous_hash': previous_hash or calculate_hash(blockchain[-1]),
    }
    block['hash'] = calculate_hash(block)
    return block

# Function to verify the integrity of the blockchain
def verify_blockchain():
    for i in range(1, len(blockchain)):
        if blockchain[i]['previous_hash'] != calculate_hash(blockchain[i - 1]):
            return False
    return True

# Initialize blockchain with genesis block
blockchain = [create_block("Genesis Block", None)]

# Function to add block to Google Sheets
def add_block_to_sheet(block):
    sheet.append_row([block['index'], block['timestamp'], block['vote'], block['previous_hash'], block['hash']])

# Function to retrieve blocks from Google Sheets
def get_blocks_from_sheet():
    return sheet.get_all_records()

# Function to add a vote
def add_vote(vote):
    previous_hash = blockchain[-1]['hash']
    new_block = create_block(vote, previous_hash)
    add_block_to_sheet(new_block)
    blockchain.append(new_block)

# Function to display all votes
def display_votes():
    blocks = get_blocks_from_sheet()
    for block in blocks[1:]:
        print("Block:", block['index'])
        print("Timestamp:", block['timestamp'])
        print("Vote:", block['vote'])
        print("Previous Hash:", block['previous_hash'])
        print("Hash:", block['hash'])
        print()

# Function to count votes
def count_votes():
    blocks = get_blocks_from_sheet()
    vote_count = {}
    for block in blocks[1:]:
        candidate = block['vote']
        if candidate in vote_count:
            vote_count[candidate] += 1
        else:
            vote_count[candidate] = 1
    return vote_count

# List of candidates
candidates = ["Candidate A", "Candidate B", "Candidate C"]

# Function to display candidates
def display_candidates():
    print("Candidates List:")
    for i, candidate in enumerate(candidates):
        print(f"{i + 1}. {candidate}")

# User input loop
while True:
    print("\nOptions:")
    print("1. Vote")
    print("2. Display Votes")
    print("3. Display Candidates")
    print("4. Display Vote Count")
    print("5. Verify Blockchain")
    print("6. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        display_candidates()
        vote = int(input("Enter the number of the candidate you want to vote for: "))
        if vote >= 1 and vote <= len(candidates):
            add_vote(candidates[vote - 1])
            print("Vote added successfully!")
        else:
            print("Invalid candidate number!")
    elif choice == "2":
        display_votes()
    elif choice == "3":
        display_candidates()
    elif choice == "4":
        print("Vote Count:")
        vote_count = count_votes()
        for candidate, count in vote_count.items():
            print(f"{candidate}: {count}")
    elif choice == "5":
        print("Blockchain is valid:", verify_blockchain())
    elif choice == "6":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 6.")
