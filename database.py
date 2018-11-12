class Table():
    '''A class to represent a SQuEaL table'''

    def __init__(self, new_dict={}):
        '''
        (Table) -> NoneType
        Create a table with columns and rows, where the key of a dictionary
        is the column, and the list of values is the row.
        '''
        self._table = new_dict

    def __str__(self):
        '''
        (Table) -> str
        Return the table as a string representation.
        '''
        return str(self._table)

    def multiply_rows(self, table2):
        '''
        (Table, Table) -> dict of {str: list}
        REQ: Both tables have dictionaries which are non-empty
        REQ: Both tables are unique
        Given two tables, return a dictionary which merges the dictionaries
        of the two tables. Their rows will be multiplied with one another. The
        rows will be paired in such a way so that if one column has under it
        [1,2,3,4] and a column from the other table has [1,2,3] column 1 will
        be [1,1,1,2,2,2,3,3,3,4,4,4] and column 2 will have under it
        [1,2,3,1,2,3,1,2,3,1,2,3] so that each row will be paired with a
        unique row and all possibilities are used.
        '''
        table1_rows = self.num_rows()
        table2_rows = table2.num_rows()

        # Loop through every column in the first table to multiply its rows
        # Get the elements in each of the table's dictionaries' lists to
        # be in the form [1,2,3,4,1,2,3,4...] depending on the other table
        for key in self._table:
            # Add i elements to the current column so there is a total
            # of x rows where x is number of rows in 1st table * number of
            # rows in 2nd tableand i is x subtract the current number of
            # rows in the column
            for i in range(0, (table1_rows * table2_rows) - table1_rows):
                # Repeatedly add the elements of the row to the column
                self._table[key].append(self._table[key][i])

        # For table 2, create a new empty dict to copy its elements
        new_dict = {}
        # Loop through every column in table2 to get the key of its dict
        # The goal is to make a dict to that each of the dictionaries'
        # lists will be in the form [1,1,1,2,2,2,3,3,3...] depending on
        # the other table's dictionary
        for key in table2._table:
            # Assign every key to an empty list for now
            new_dict[key] = []
            # Outer loop will loop for every number of rows table2 has
            for i in range(0, table2_rows):
                # Inner loop loops for every number of rows table1 has
                for j in range(0, table1_rows):
                    # Append an element of table2's list to the new dict
                    new_dict[key].append(table2._table[key][i])
        # Combine the tables by adding the keys and values of the new dict
        # to table1's dict
        for key in new_dict:
            self._table[key] = new_dict[key]
        # Return a dictionary which will be made into a table in the function
        return self._table

    def cartesian_zero_rows(self, table2):
        '''
        (Table, Table) -> Table
        Returns a table with empty rows.
        '''
        # Add every column from table2 into table1
        for key in table2._table:
            self._table[key] = table2._table[key]
        # Since 0 times any number is 0, there will be 0 rows
        # Make the rows empty
        for key in self._table:
            self._table[key] = []
        return self

    def select_column(self, columns):
        '''
        (Table, list of str) -> Table
        Given a table and a list of column names, return a table with only
        those column names remaining.
        '''
        # Make a copy of the table's dictionary
        table_copy = self._table
        # Make the table's dictionary empty
        self._table = {}
        # Cover every key in what was once the table's dictionary
        for key in table_copy:
            # If the key is in the list of desired column names, add it back
            # into the table's dictionary. This way, any column name that
            # was not in the list will be left out in the end.
            if(key in columns):
                # Add the key and value back into the dictionary
                self._table[key] = table_copy[key]
        return self

    def column_equal(self, col1, col2):
        '''
        (Table, str, str) -> Table
        Given a table and two column names, return a modified table with
        only rows of the two columns which have equal values remaining.
        '''
        # Create an index list to store the indexes where rows' values' match
        indexList = []
        # Loop through all the rows of both columns and find matching values
        for i in range(0, self.num_rows()):
            # Save the indexes of any values which match
            if(self._table[col1][i] == self._table[col2][i]):
                indexList.append(i)
        # Make a new table object
        new_list = Table()
        # Copy any values of the previous tables which match to the new table
        for key in self._table:
            # Start by making an empty list for each key value
            new_list._table[key] = []
            for i in range(self.num_rows()):
                # Append the values at the index of the matching rows to list
                if(i in indexList):
                    new_list._table[key].append(self._table[key][i])
        # Return the new table which has the desired rows
        return new_list

    def column_greater(self, col1, col2):
        '''
        (Table, str, str) -> Table
        Given a table and two column names, return a modified table with
        only rows where the first column is greater than the second column.
        '''
        # Create an index list to store the indexes where rows' values' match
        indexList = []
        # Loop through all the rows of both columns and find where col1 is
        # greater than col2
        for i in range(0, self.num_rows()):
            # Save the indexes of any values which satisfy the condition
            if(self._table[col1][i] > self._table[col2][i]):
                indexList.append(i)
        # Make a new table object
        new_list = Table()
        # Copy any values of the previous tables which match to the new table
        for key in self._table:
            # Start by making an empty list for each key value
            new_list._table[key] = []
            for i in range(self.num_rows()):
                # Append the values at the index of the matching rows to list
                if(i in indexList):
                    new_list._table[key].append(self._table[key][i])
        # Return the new table which has the desired rows
        return new_list

    def compare_value_equal(self, col1, val):
        '''
        (Table, str, float) -> Table
        Given a table, a column name and a value, return a modified table
        where only rows which satisfy the constraint remain. Rows which are
        equal to the value given by the constraint will remain in this case.
        '''
        # Make a list to store the indexes
        indexList = []
        # loop through every element of the column
        # Attempt to make the current index into a float
        try:
            for i in range(0, self.num_rows()):
                # Make a temporary variable to store the value of the element
                temp = self._table[col1][i]
                # Make the variable into a float
                temp = temp.strip("'")
                temp = float(temp)
                # If the variable is equal to the value of the constraint
                # argument, add that index to the list
                if(temp == val):
                    indexList.append(i)
        # Skip the attempt if it is not possible
        except:
            pass
        # Make a new table
        new_table = Table()
        # Go through every key in the original table's dictionary
        for key in self._table:
            new_table._table[key] = []
            # Add the values to the new table's dictionary at each matching
            # index from the original table's dictionary
            for i in range(self.num_rows()):
                if(i in indexList):
                    new_table._table[key].append(self._table[key][i])
        return new_table

    def compare_value_greater(self, col1, val):
        '''
        (Table, str, float) -> Table
        Given a table, column name and value, return a modified table where
        only rows which satisfy the constraint remain. Rows which are greater
        than the value given by the constraint will remain in this case.
        '''
        # Make a list to store the indexes
        indexList = []
        # loop through every element of the column
        for i in range(0, self.num_rows()):
            # Attempt to make the current index into a float
            try:
                # Make a temporary variable to store the value of the element
                temp = self._table[col1][i]
                # Make the variable into a float
                temp = temp.strip("'")
                temp = float(temp)
                # If the variable is greater than the value of the constraint
                # argument add that index to the list
                if(temp > val):
                    indexList.append(i)
            # Skip the attempt if it is not possible
            except:
                pass
        # Make a new table
        new_table = Table()
        # Go through every key in the original table's dictionary
        for key in self._table:
            new_table._table[key] = []
            # Add the values to the new table's dictionary at each matching
            # index from the original table's dictionary
            for i in range(self.num_rows()):
                if(i in indexList):
                    new_table._table[key].append(self._table[key][i])
        return new_table

    def set_dict(self, new_dict):
        '''(Table, dict of {str: list of str}) -> NoneType

        Populate this table with the data in new_dict.
        The input dictionary must be of the form:
            column_name: list_of_values
        '''
        self._table = new_dict

    def get_dict(self):
        '''(Table) -> dict of {str: list of str}

        Return the dictionary representation of this table. The dictionary keys
        will be the column names, and the list will contain the values
        for that column.
        '''
        return self._table

    def num_rows(self):
        '''
        (Table) -> int
        REQ: Each column has same amount of rows with information
        Return the amount of rows in a table. This is assuming that each
        column in the table has the same number of rows.
        '''
        # Make an empty list to store keys from the table object
        self.keyList = []
        # Add each key to the list in no particular order
        for key in self._table:
            self.keyList.append(key)
        # Make the variable equal to a random keys' value, which is a list
        self.row_var = self._table[self.keyList[0]]
        # The number of rows will equal the length of the list
        self._rows = len(self.row_var)
        return self._rows

    def print_csv(self):
        '''(Table) -> NoneType
        Print a representation of table in csv format.
        '''
        # no need to edit this one, but you may find it useful (you're welcome)
        dict_rep = self.get_dict()
        columns = list(dict_rep.keys())
        print(','.join(columns))
        rows = self.num_rows()
        for i in range(rows):
            cur_column = []
            for column in columns:
                cur_column.append(dict_rep[column][i])
            print(','.join(cur_column))


class Database():
    '''A class to represent a SQuEaL database'''

    def __init__(self, new_dict={}):
        '''
        (Database) -> NoneType
        Create a new table. Contains columns (dict key) and rows(dict value).
        '''
        self._new_dict = new_dict

    def __str__(self):
        '''
        (Database) -> str
        Return the database as a string representation.
        '''
        return str(self.get_dict())

    def return_table(self, table_name):
        '''
        (Database, str) -> Table
        Return a table from the database.
        '''
        new_table = self._new_dict[table_name]
        return new_table

    def set_dict(self, new_dict):
        '''(Database, dict of {str: Table}) -> NoneType

        Populate this database with the data in new_dict.
        new_dict must have the format:
            table_name: table
        '''
        self._new_dict = new_dict

    def get_dict(self):
        '''(Database) -> dict of {str: Table}

        Return the dictionary representation of this database.
        The database keys will be the name of the table, and the value
        with be the table itself.
        '''
        return self._new_dict
