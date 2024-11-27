import sqlite3

try:
    conn = sqlite3.connect("BMS.db")
    cursor = conn.cursor()

    # Query to get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if not tables:
        print("No tables found in the database.")

    # Loop through each table and print its contents
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()

        # Fetch column names
        column_names = [description[0] for description in cursor.description]
        print(f"Columns: {', '.join(column_names)}")
        for row in rows:
            print(row)

    conn.close()
except Exception as e:
    print(f"An error occurred: {e}")
