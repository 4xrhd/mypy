import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Add the credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('access.json', scope)

# Authorize the clientsheet 
client = gspread.authorize(creds)

# Get the instance of the Spreadsheet
sheet = client.open('ims').sheet1

def menuDisplay():
    print('=============================')
    print('= Inventory Management Menu =')
    print('=============================')
    print('(1) Add New Item to Inventory')  
    print('(2) Remove Item from Inventory')
    print('(3) Update Inventory')
    print('(4) Search Item in Inventory')
    print('(5) Print Inventory Report')
    print('(99) Quit')
    CHOICE = int(input("Enter choice: "))
    menuSelection(CHOICE)

def menuSelection(CHOICE):
    if CHOICE == 1:
        addInventory()
    elif CHOICE == 2:
        removeInventory()
    elif CHOICE == 3:
        updateInventory()
    elif CHOICE == 4:
        searchInventory()
    elif CHOICE == 5:
        printInventory()
    elif CHOICE == 99:
        exit()

def addInventory():
    print("Adding Inventory")
    print("================")
    item_description = input("Enter the name of the item: ")
    item_quantity = input("Enter the quantity of the item: ")

    # Append the data to the Google Sheet
    sheet.append_row([item_description, item_quantity])
    
    CHOICE = int(input('Enter 98 to continue or 99 to exit: '))
    if CHOICE == 98:
        menuDisplay()
    else:
        exit()
    
def removeInventory():
    print("Removing Inventory")
    print("==================")
    item_description = input("Enter the item name to remove from inventory: ")
    cell = sheet.find(item_description)
    sheet.delete_row(cell.row)
    
    CHOICE = int(input('Enter 98 to continue or 99 to exit: '))
    if CHOICE == 98:
        menuDisplay()
    else:
        exit()

def updateInventory():
    print("Updating Inventory")
    print("==================")
    item_description = input('Enter the item to update: ')
    item_quantity = int(input("Enter the updated quantity. Enter - for less: "))

    cell = sheet.find(item_description)
    old_quantity = int(sheet.cell(cell.row, cell.col + 1).value)
    new_quantity = old_quantity + item_quantity

    sheet.update_cell(cell.row, cell.col + 1, new_quantity)
                                            
    CHOICE = int(input('Enter 98 to continue or 99 to exit: '))
    if CHOICE == 98:
        menuDisplay()
    else:
        exit()

def searchInventory():
    print('Searching Inventory')
    print('===================')
    item_description = input('Enter the name of the item: ')
    
    cell = sheet.find(item_description)
    print('Item:     ', sheet.cell(cell.row, cell.col).value)
    print('Quantity: ', sheet.cell(cell.row, cell.col + 1).value)
    print('----------')
        
    CHOICE = int(input('Enter 98 to continue or 99 to exit: '))
    if CHOICE == 98:
        menuDisplay()
    else:
        exit()
        
def printInventory():
    print('Current Inventory')
    print('-----------------')
    for row in sheet.get_all_values():
        print('Item:     ', row[0])
        print('Quantity: ', row[1])
        print('----------')

    CHOICE = int(input('Enter 98 to continue or 99 to exit: '))
    if CHOICE == 98:
        menuDisplay()
    else:
        exit()

menuDisplay()

