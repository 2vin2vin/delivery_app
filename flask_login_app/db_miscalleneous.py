import sqlite3

def table_list():
    out=[]
    conn = sqlite3.connect('./instance/users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for t in tables:
        out.append(t[0])

    conn.close()
    return out

def get_all_tables():
    t_list = table_list()
    conn = sqlite3.connect('./instance/users.db')
    cursor = conn.cursor()
    for i in t_list:
        # Define the table name and ID value
        table_name = i
        specific_id = 1  # Replace with your actual ID
        try:

            # Execute a query to select data for the specific ID
            cursor.execute(f"SELECT * FROM {table_name} ")
            rows = cursor.fetchall()
            # Print the fetched rows
            print("In db_miscellaneous")
            print(i)
            print(len(rows))
            for row in rows:
                print(row)
        except Exception as e:
            print("error:",e)
    
def get_id_from_table(table_name=None, column=None):
    conn = sqlite3.connect('./instance/users.db')
    cursor = conn.cursor()
    try:
        # Execute a query to select data for the specific ID
        cursor.execute(f"SELECT {column} FROM {table_name} ")
        rows = cursor.fetchall()
        for row in rows:
            last_id=row
    except Exception as e:
        print("error:",e)
    conn.close()
    try:
        return int(last_id[0][2:]) + 1
    except:
        return 0

def get_length_table(table_name=None):
    conn = sqlite3.connect('./instance/users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for t in tables:
        if table_name != None:
            if t[0] == table_name:
                cursor.execute(f"SELECT * FROM {table_name} ")
                rows = cursor.fetchall()
                return len(rows)
    return 0

def print_schema(user='user'):
    # Connect to your SQLite database
    conn = sqlite3.connect('./instance/users.db')  # Replace with your database path
    cursor = conn.cursor()

    # Execute PRAGMA command to get table schema
    cursor.execute("PRAGMA table_info({});".format(user))

    # Fetch and print the schema
    schema = cursor.fetchall()
    for column in schema:
        print(column)

    # Close the connection
    conn.close()
#print(int(get_id_from_table(table_name='user',column='id')[0][2:]))
get_all_tables()