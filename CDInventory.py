#------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# TMcFarland, 2021-Feb-19, started mods: adding functions, addressed existing TODOs
# TMcFarland, 2021-Feb-28, made code updates as suggested by DKlos for Assignment 6
# TMcFarland, 2021-Feb-28, changed data save & retreval to pickeld .dat file
# TMcFarland, 2021-Feb-28, introduced error handling with user entry and checking for exisiting database.
#------------------------------------------#

#Importing os.path for additional FileProcessor.read_file functionality, to check to see if text file exists
import os.path, pickle #, shelve

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of dicts to hold data
dicRow = {}  # dict of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    @staticmethod
    def delete_dict(delDict, table):
        """Deletes lstTbl dicitonary entry based on user input of ID number
        Args:
            delDict (integer): ID number representing table entry

        Returns:
            NONE
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == delDict:
                # Again here we're using the local value of table
                # del lstTbl[intRowNr]
                del table[intRowNr]
                blnCDRemoved = True
                break

        # Return the delete status
        return blnCDRemoved


    @staticmethod
    def append_table(intID, strTitle, strArtist, table):
        # 3.3.2 Add item to the table
        """Takes arguments from Main loop append section and appends to 'table'.
            Because this is a list, and lists are references, changes made to local variable 'table'
            will automatically update the original list, as they are the same thing in memory
        Args:
            intID (string): ID number
            strTitle (string): CD title
            StrArtist (string); Artist Name
            table (list); list of dictionary entries of above data

        Returns:
            None
        """
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
        # Append to the table passed in.  Since lstTbl is passed as a reference type,
        # we do not have to return it.
        table.append(dicRow)


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts). One line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            fileCreate (Bool) If true, Binary file didn't exist and was created'
        """
        table.clear()  # this clears existing data and allows to load data from file
        #check to see if database file already exists. If not, create blank one.
        fileCreate = False
        if os.path.exists('CDInventory.dat'):
            try:
                f = open(file_name, 'rb')
                table = pickle.load(f)
                f.close()
            except EOFError as e:
                print('Your CDInventory.dat file is blank!')
                print('Here\'s what the computer has to say about this:')
                print(type(e), e, e.__doc__, sep = '\n') #syntax from FDN_Py_module_07, pg 20, listing 12

        else:
            #create blank database in same folder as script
            objFile = open(strFileName, 'w')
            objFile.close()
            fileCreate = True
        return fileCreate, table

    @staticmethod
    def write_file(table):
        """Writes List of Dicitonaries lstTbl from memory into a text file.
        Ensures proper comma seperated formatting for best storage and retrieval
        Args:
            None

        Returns:
            None
        """
        f = open('CDInventory.dat', 'wb')
        pickle.dump(table, f)
        f.close()


# -- PRESENTATION (Input/Output) -- #
class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.
        """

        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def user_cd_input():
        """ Receives user input for CD ID number, Album Title, and Artist Name
        Args:
            None
        Returns:
            All strings: CD ID number, CD Title, CD Artist Name
        """

        # 3.3.1 Ask user for new ID, CD Title and Artist
        while True:
            try:
                intID = int(input('Enter ID: ').strip())
                break
            except ValueError as e:
                print('That does not appear to be an integer. Try again.')
                print('Here\'s what the computer has to say about this:')
                print(type(e), e, e.__doc__, sep = '\n') #syntax from FDN_Py_module_07, pg 20, listing 12
            except Exception as e:
                print('There was some sort of general error, please try again')
                print('Here\'s what the computer has to say about this:')
                print(type(e), e, e.__doc__, sep = '\n')
        while True:
            strTitle = input('What is the CD\'s title? ').strip()
            if strTitle == '':
                print('For the love of God, please enter *something*')
                continue
            else:
                break
        while True:
            strArtist = input('What is the Artist\'s name? ').strip()
            if strArtist == '':
                print('For the love of God, please enter *something*')
                continue
            else:
                break
        return intID, strTitle, strArtist


# -- MAIN PROGRAM -- #
# 1. When program starts, read in the currently saved Inventory
noDatFilePresent, lstTbl = FileProcessor.read_file(strFileName, lstTbl)
#check to see if  FileProcessor.read_file returned a Bool of True. if so, DB file didn't exist
if noDatFilePresent:
    print('\nCDInventory.dat didn\'t exist in folder. A blank version has been created\n')

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection

    # 3.1 EXIT process exit first
    if strChoice == 'x':
        break

    # 3.2 LOAD process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...\n')
            fileCreate, lstTbl = FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.\n')
            IO.show_inventory(lstTbl)
        continue

    # 3.3 ADD CD process add a CD
    elif strChoice == 'a':
        #assign received data from user variables from return of IO.user_cd_input
        recIntId, recStrTitle, recStrArtist = IO.user_cd_input()
        #Feed received data from user into DataProcessor.append_table
        DataProcessor.append_table(recIntId, recStrTitle, recStrArtist, lstTbl)
        IO.show_inventory(lstTbl)
        continue

    # 3.4 DISPLAY INVENTORY process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue

    # 3.5 DELETE process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        intIDDel = int(input('Which ID would you like to delete? ').strip())
        # 3.5.2 search thru table and delete CD

        cd_removed = DataProcessor.delete_dict(intIDDel, lstTbl)

        # Using that returned bool we can now display the delete status.
        if cd_removed: #could add '== True', but this is more efficient
            print('The CD was removed\n')
        else:
            print('Could not find this CD!\n')

        IO.show_inventory(lstTbl)
        continue

    # 3.6 SAVE process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y' or 'yes':
            FileProcessor.write_file(lstTbl)
            print('Saved to file\n')
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue

    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')
