# Functions for reading tables and databases

import glob
from database import *


file_list = glob.glob('*.csv')


# Write the read_table and read_database functions below
def read_table(file_name):
    '''
    (str) -> Table
    REQ: file_name is a .csv file
    Given a txt file, this function will read the file and make a dictionary
    then return the text as a table object. Each key will be mapped to a list;
    the pair will represent one column of the table.
    '''
    # Open the file to read, and read the text into a list
    lines = open(file_name, 'r')
    file_text = lines.readlines()
    # Close the file
    lines.close()
    # Go through each element of the list and remove new lines
    for i in range(0, len(file_text)):
        file_text[i] = file_text[i].strip('\n')
        # Delete any empty lines
        if (file_text[i] is ""):
            del file_text[i]
    # Make a dictionary representing a table
    table = {}
    # Make a list containing the keys, which should be the first line of
    # the file. They are the headers of the columns in a table.
    listKeys = file_text[0].split(',')
    # Create a new list and make each line of the file an element in it
    # The contents of the list are the remaining lines of the file, and
    # they contain the title, author, year, etc of the movie/book
    listContent = []
    for i in range(1, len(file_text)):
        listContent.append(file_text[i].split(','))
    # Create a nested loop to map each key with a list
    for i in range(0, len(listKeys)):
        # Make key number i be mapped to an empty list for now
        table[listKeys[i]] = []
        # Map each key to a list of a specific category (i.e year, author)
        for j in range(0, len(listContent)):
            # Strip any leading white space and add a value to the key
            listContent[j][i] = listContent[j][i].strip()
            table[listKeys[i]] = table[listKeys[i]] + \
                [listContent[j][i]]
    # Make a new instance of Table()
    my_table = Table(table)
    return my_table


def read_database():
    '''
    () -> Database
    REQ: Must have unique table names
    REQ: Directory should have table files
    Read all .csv files in the directory and return a Database object
    representing the data from the files.
    '''
    # Make a dictionary representing database
    database = {}
    # Create a list to store the data of the files
    data_table = []
    # Make new list for the name of the files
    table_name = []
    for i in range(0, len(file_list)):
        # Create an i amount of tables one by one
        data_table.append(read_table(file_list[i]))
        # Remove the '.csv' from the end of the file name and add it to list
        table_name.append(file_list[i].replace('.csv', ''))
    # Populate the dictionary using the lists
    for i in range(0, len(table_name)):
        database[table_name[i]] = data_table[i]
    # Create a new instance of Database() using the dictionary
    my_database = Database(database)
    return my_database
