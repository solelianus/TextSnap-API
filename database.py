import sqlite3

# Path to your SQLite database file
DB_FILE = "fonts.db"

def check_table_schema(table_name):
    try:
        # Connect to the database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Execute the PRAGMA command to get table schema
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        # Print the schema
        print(f"Schema for table '{table_name}':")
        for column in columns:
            print(f"Column Name: {column[1]}, Type: {column[2]}, Not Null: {bool(column[3])}, Default Value: {column[4]}")

    except Exception as e:
        print(f"Error checking schema: {e}")

    finally:
        # Close the connection
        conn.close()

# Replace 'fonts' with the name of the table you want to inspect
check_table_schema("fonts")