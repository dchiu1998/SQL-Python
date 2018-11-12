from reading import *
from database import *

# Below, write:
# *The cartesian_product function
# *All other functions and helper functions
# *Main code that obtains queries from the keyboard,
#  processes them, and uses the below function to output csv results
# Below are the indexes which each token of the query should be in
table_index = 3
column_index = 1
constraint_index = 5


def run_query(database, query):
    '''
    (Database, str) -> Table
    REQ: database is a dictionary containing tables
    REQ: query is in the correct specific syntax
    Given a query, this function runs the query on the database and returns
    a table of the corresponding results.
    >>> run_query(read_database(), "select * from books")
    book.author,book.title,book.year
    Douglas Hofstadter,Godel Escher Bach,1979
    Randall Munroe,What if?,2014
    Randall Munroe,Thing Explainer,2015
    Andrew Hodges,Alan Turing: The Enigma,2014
    >>> run_query (read_database(), "select book.title,book.year from /
    books where book.year>'2014'")
    book.title,book.year
    Thing Explainer,2015
    >>> run_query(read_database() "select * from books,olympics-locations /
    where l.year=book.year")
    book.year,l.city,l.country,book.title,book.author,l.year
    2014,Sochi,Russia,What if?,Randall Munroe,2014
    2014,Sochi,Russia,Alan Turing: The Enigma,Andrew Hodges,2014
    '''
    # Split up parts of the query into tokens of a list
    listTokens = query.split()
    # SIDE NOTE: column name(s) = index 1; table name(s) = index 3
    # constraint(s) = index 5 GLOBAL VARS AVAILABLE
    # Get a list of all the table names
    table_names = get_tables(listTokens)
    # Get a list of all the columns
    column_names = get_columns(listTokens)
    # Create a table object
    display_table = Table()
    # There should be atleast 1 table name, so get that table
    display_table = database.return_table(table_names[0])
    # If there is more than 1, multiply the rows of all the tables
    if(len(table_names) > 1):
        list_counted = False
        count = 0
        # Loop until the contents of the list containing the names of the
        # tables is exhausted
        while (list_counted is False):
            # table1 will be the current table
            table1 = display_table
            # table2 will the te next table in the list
            table2 = database.return_table(table_names[count + 1])
            # Call cartesian_product to multiply the tables
            display_table = cartesian_product(table1, table2)
            count = count + 1
            # Exit once everything in the list has been multiplied
            if(count == len(table_names) - 1):
                list_counted = True
    # If there is a 'where' in the query, this if statement will run
    if('where' in listTokens):
        # Create a list of the constraints
        constraints = get_constraints(listTokens)
        # Send in the table and constraints one at a time to modify the table
        for i in range(0, len(constraints)):
            display_table = breakdown_constraints(display_table,
                                                  constraints[i])
    # Call the method to get grab specific columns only if "*" is not after
    # the select token
    if ("*" not in column_names):
        display_table.select_column(column_names)
    # Return the final table result
    return display_table


def cartesian_product(table1, table2):
    '''
    (Table, Table) -> Table
    REQ: Each table has a dictionary
    REQ: There are more than 0 rows in each Table
    REQ: Each table has its own equal amount of rows in each column
    Given two tables, this function multiplies the rows and returns
    a new table which is the product of the two.
    >>> dict1 = {'A':[1,2], 'B':[3,4]}
    >>> dict2 = {'C':['a','b'], 'D':['c','d']}
    >>> table1 = Table()
    >>> table2 = Table()
    >>> table1.set_dict(dict1)
    >>> table2.set_dict(dict2)
    >>> result = cartesian_product(table1, table2)
    >>> expected = {'A':[1,2,1,2], 'B':[3,4,3,4] 'C':['a','a','b','b'] /
    'D':['c','c','d','d']}
    >>> result._table == expected
    True
    >>> dict1 = {'col1': [], 'col2': [] 'col3' = []}
    >>> dict2 = {'col4': [1,2], 'col5' = ['a','b']}
    >>> table1 = Table()
    >>> table2 = Table()
    >>> table1.set_dict(dict1)
    >>> table2.set_dict(dict2)
    >>> result = cartesian_product(table1, table2)
    >>> expected = {'col1': [], 'col2': [] 'col3': [] 'col4': [] 'col5': []}
    >>> result._table == expected
    True
    '''
    # If table1 or table2 has 0 rows, call this method
    if(table1.num_rows == 0 or table2.num_rows == 0):
        table_product = table_product.cartesian_zero_rows(table2)
    # Otherwise, call table_product to multiply the rows and merge the tables
    else:
        table_product = table1.multiply_rows(table2)
        table_product = Table(table_product)
    return table_product


def breakdown_constraints(table, constraint):
    '''
    (Table, str) -> Table
    REQ: Table has a dict with more than 0 rows
    REQ: constraint is a str with valid column names and operator
    Given a table and a constraint, modify to table so that it satisfies
    the condition of the constraint.
    '''
    # Call the column_equal method if there is a "=" in the constraint
    if("=" in constraint):
        # Remove "=" from the list since it is now known there was an "="
        listConditions = constraint.split("=")
        # There should be 2 elements left in the list; assign values to each
        col1 = listConditions[0]
        col2 = listConditions[1]
        # Check to see if the user entered a hard coded value
        # Only after the operator can a value be hard coded, so check 2nd item
        try:
            col2 = col2.strip("'")
            col2 = float(col2)
        # Move on if it isn't one
        except:
            pass
        # If the user entered a float, call this method to modify table
        if(type(col2) is float):
            table = table.compare_value_equal(col1, col2)
        # Otherwise, call the column_equal method
        else:
            table = table.column_equal(col1, col2)
    # Call the column_greater method if there is a ">" in the constraint
    if(">" in constraint):
        # Remove the ">" and assign the 2 conditions to a variable each
        listConditions = constraint.split(">")
        col1 = listConditions[0]
        col2 = listConditions[1]
        # Check to see if the user entered a hard coded value
        try:
            col2 = col2.strip("'")
            col2 = float(col2)
        # Continue normally if not
        except:
            pass
        # If the user entered a float, call this method to modify table
        if(type(col2) is float):
            table = table.compare_value_greater(col1, col2)
        # Otherwise, call the column_greater method
        else:
            table = table.column_greater(col1, col2)
    # Return the new table
    return table


def num_rows(table):
    '''
    (Table) -> int
    REQ: Each column has same amount of rows with information
    Return the amount of rows in a table. This is assuming that each
    column in the table has the same number of rows.
    >>> dict = Table()
    >>> dict._table = {'A':[1,2,3,4,5], 'B':[5,4,3,2,1]}
    >>> result = num_rows(dict)
    >>> result == 5
    True
    '''
    # Make an empty list to store keys from the table object
    keyList = []
    # Add each key to the list in no particular order
    for key in table:
        keyList.append(key)
    # Make the variable equal to a random keys' value, which is a list
    row_var = table[keyList[0]]
    # The number of rows will equal the length of the list
    rows = len(row_var)
    return rows


def get_tables(tokens):
    '''
    (list of str) -> list of str
    REQ: tokens is a list containing strings in proper query order
    Given a list of tokens, return a list of table names at a specific
    index. The index will be a fixed value, since it is assumed that the
    list is in proper format based on the query.
    >>> get_tables(["select", "columnA,columnB", "from", "movieA,movieB"])
    ["movieA", "movieB"]
    >>> get_tables(["select", "columnA,columnB", "from", "movieC"])
    ["movieC"]
    '''
    # Split tokens at index 3 with "," to get a list of table names
    tables = tokens[table_index].split(',')
    return tables


def get_constraints(tokens):
    '''
    (list of str) -> list of str
    REQ: tokens is a list containing strings in proper query order
    Given a list of tokens, return a list of the constraints specified by
    the query. Constraints should be seperated by "," in a fixed index.
    >>> get_constraints(["select", "*", "from" "book", "where", /
    "book.year>'1900'"])
    ["book.year>'1900'"]
    >>> get_constraints(["select", "*", "from" "movie", "where", /
    "movie.year>'2010,movie.title='Startrek''"])
    ["movie.year>'2010', "movie.title='Startrek'""]
    '''
    constraints = tokens[constraint_index].split(',')
    return constraints


def get_columns(tokens):
    '''
    (list of str) -> list of str
    REQ: tokens is a list containing strings in proper query order
    Given a list of tokens, return a list containing all the column names
    specified by the query. Columns should be at a fixed index position.
    >>> get_columns(["select", "columnA,columnB", "from", "movieA,movieB"])
    ["columnA", "columnB"]
    >>> get_column(["select", "columnD", "from", "movieA,movieB"])
    ["columnD"]
    '''
    columns = tokens[column_index].split(',')
    return columns


if(__name__ == "__main__"):
    exit = False
    while not exit:
        query = input("Enter a SQuEaL query, or a blank line to exit:")
        if(query != ''):
            run_query(read_database(), query).print_csv()
        else:
            exit = True
