import sqlite3
import os
import re


class DBHandler:
    def __init__(self, database_name="a3.db"):
        self.db_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db')
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.database = os.path.join(self.db_dir, database_name)
        self.schema = os.path.join(self.db_dir, 'schema.sql')
        self.datafile_ext = ['.data']

    '''
       Database controller can be used in 3 modes:
       1. Bind mode: Arguments are bound in command. NOTE any command with 7 or more arguments MUST USE BIND MODE !
       2. Non-bind single mode: Execute one single command, fetch the result.
       3. Non-bind multiple mode: Execute multiple commands, NO RESULT can be fetched (return empty list).
    '''
    def database_controller(self, command, mode='non-bind', values=None):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        try:
            if mode == 'bind':
                cursor.execute(command, values)
            elif len(re.findall(';', command)) > 1:
                cursor.executescript(command)
            else:
                cursor.execute(command)
        except (sqlite3.OperationalError, sqlite3.ProgrammingError) as error:
            print('[Error] During executing SQL command, an error raised: ', error)
            print('[Error] This command failed: ', command)
            return False
        else:
            result = cursor.fetchall()
            connection.commit()
            connection.close()
            return result

    def get_column_names(self, table):
        result = self.database_controller(f"PRAGMA table_info('{table}')")
        names = list()
        if result:
            for attributes in result:
                names.append(attributes[1])
            return names
        return False

    def initialize(self):
        if os.path.exists(self.database):
            print('Database already exists.')
            return False
        if not os.path.exists(self.schema):
            print('Schema does not exist!')
            return False

        print(f"Initializing database ...")
        with open(self.schema, 'r') as schema:
            sql_file = schema.read()
            sql_scripts = sql_file.split(';')
            for command in sql_scripts:
                self.database_controller(command + ';')
        print("Database successfully initialized.")
        return True

    def data_import(self):
        data_files = os.listdir(self.data_dir)
        for files in data_files:
            if os.path.splitext(files)[-1] not in self.datafile_ext:
                continue
            print(f"Importing data from '{files}' ...")
            with open(os.path.join(self.data_dir, files), 'r') as file:
                for line in file:
                    if re.findall('[\?a-zA-Z]', line):
                        continue
                    nums = line.rstrip('\n').split(',')
                    command = 'INSERT INTO Rawdata VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);'
                    values = tuple([float(x) for x in nums])
                    self.database_controller(command, mode='bind', values=values)
            print(f"Data from '{files}' successfully imported to database.")
