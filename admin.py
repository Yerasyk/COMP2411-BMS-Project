from datetime import datetime 
import sqlite3;
import re
import hashlib
import random
import openpyxl

REPORT_PATH="BMSReport.xlsx"
DB_PATH="BMS.db"

def isValidEmail(email):
    return re.match(r'^.+@.+\..+$', email)

def standartName(name):
    return name.lower().capitalize()

def hashingPassw(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def create_admin_account():
    try:
        #Handling inputs
        email=input("Write your email: ").strip()
        if(isValidEmail(email)==None):
            return "Email address isn't valid."
        
        name=input("Write your name: ").strip()
        name=standartName(name)

        password= input("Write your password: ").strip()
        hashed_password=hashingPassw(password)

        #Inserting into table
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO Administrator (Email, Name, Password)
        VALUES (?, ?, ?);
        """, (email, name, hashed_password))

        conn.commit()
        conn.close()

        return "Admin account created successfully!"
    except sqlite3.IntegrityError:
        return "Error: Admin with this email already exists."
    except Exception as e:
        return f"An error occurred: {e}"
#Log in to account
def enterAccount():
    global logged_email
    try:
        email = input("Enter your email: ").strip()
        if(isValidEmail(email)==None):
            return "Email address isn't valid."
        

        password = input("Enter your password: ").strip()
        hashed_password = hashingPassw(password)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT Email, Name FROM Administrator
        WHERE Email = ? AND Password = ?;
        """, (email, hashed_password))

        admin = cursor.fetchone()

        conn.close()

        if admin:
            logged_email=admin[0]
            return f"Login successful! Welcome, {admin[1]} (Email: {admin[0]})."
        else:
            return "Error: Invalid email or password."

    except Exception as e:
        return f"An error occurred: {e}"

def bin_exists(BIN):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if the BIN exists
        cursor.execute("SELECT 1 FROM Banquet WHERE BIN = ? LIMIT 1", (BIN,))
        exists = cursor.fetchone() is not None

        conn.close()
        return exists
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

# Function to create a new banquet
def create_banquet():
    try:
        name = input("Enter banquet name: ").strip()
        date_str = input("Enter banquet date and time (YYYY-MM-DD HH:MM): ").strip()
        date_time = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        address = input("Enter address: ").strip()
        location = input("Enter location: ").strip()
        staff_fname = input("Enter staff's first name: ").strip()
        staff_lname = input("Enter staff's last name: ").strip()
        available = input("Is the banquet available? (Y/N): ").strip().upper() == "Y"
        quota = int(input("Enter quota: "))

        BIN = str(int(datetime.now().strftime('%Y%m%d%H%M%S')) + random.randint(1000, 9999))

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO Banquet (BIN, Name, DateTime, Quota, Available, Location, Address, Staff_FName, Staff_LName)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (BIN, name, date_time.isoformat(), quota, available, location, address, staff_fname, staff_lname))
        conn.commit()
        conn.close()

        print(f"Banquet created with BIN: {BIN}")
        return BIN
    except ValueError as ve:
        print(f"Invalid input: {ve}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Function to create meals for a banquet
def create_meals(BIN):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print("Enter details for 4 meals:")
        for i in range(4):
            print(f"\nMeal {i+1}:")
            meal_type = input("Enter meal type: ").strip()
            dish_name = input("Enter dish name: ").strip()
            price = float(input("Enter price: ").strip())
            special_cuisine = input("Enter special cuisine (if any): ").strip()
            cursor.execute('''
                INSERT INTO Meal (BIN, MealID, Type, Price, DishName, SpecialCuisine)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (BIN, i, meal_type, price, dish_name, special_cuisine))
        conn.commit()
        conn.close()
        print("Meals added successfully.")
    except ValueError as ve:
        print(f"Invalid input: {ve}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Function to create drinks for a banquet
def create_drinks(BIN):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        n = 0
        while n == 0:
            n = int(input("Enter the number of drinks to add: "))
            if n == 0:
                print("There should be at least 1 drink!")

        for i in range(n):
            print(f"\nDrink {i+1}:")
            drink_type = input("Enter drink type: ").strip()
            drink_name = input("Enter drink name: ").strip()
            price = float(input("Enter price: ").strip())
            special_cuisine = input("Enter special cuisine (if any): ").strip()
            cursor.execute('''
                INSERT INTO Drink (BIN, DrinkID, Type, Price, DrinkName, SpecialCuisine)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (BIN, i, drink_type, price, drink_name, special_cuisine))
        conn.commit()
        conn.close()
        print("Drinks added successfully.")
    except ValueError as ve:
        print(f"Invalid input: {ve}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Function to create tables for a banquet
def create_tables_for_banquet(BIN):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Fetch quota for the given banquet ID
        cursor.execute("SELECT Quota FROM Banquet WHERE BIN = ?", (BIN,))
        quota_data = cursor.fetchone()
        quota = quota_data[0]

        print(f"The total quota for this banquet is: {quota} seats.")

        table_number = 1
        while quota > 0:
            print(f"\nRemaining quota: {quota} seats.")
            print(f"Adding Table {table_number}:")

            # Validate table type
            table_type = ""
            while table_type not in ["Special", "Simple"]:
                table_type = input("Enter table type (Special, VIP, Simple): ").strip().capitalize()
                if table_type not in ["Special", "Simple"]:
                    print("Invalid table type. Please choose 'Special', 'VIP', or 'Simple'.")

            price = float(input("Enter price: ").strip())

            seat_number = 0
            while seat_number <= 0 or seat_number > quota:
                seat_number = int(input(f"Enter seat number (1 to {quota}): "))
                if seat_number > quota:
                    print("Seat number cannot exceed the remaining quota.")
                elif seat_number <= 0:
                    print("Seat number must be greater than 0.")

            cursor.execute('''
                INSERT INTO Tables (BIN, Table_Number, SeatQuantity, TableType, Price)
                VALUES (?, ?, ?, ?, ?)
            ''', (BIN, table_number, seat_number, table_type, price))

            quota -= seat_number
            table_number += 1

        conn.commit()
        conn.close()
        print("Tables added successfully.")
    except ValueError as ve:
        print(f"Invalid input: {ve}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Function to assign an admin to a banquet
def assign_admin_to_banquet(BIN):
    try:
        global logged_email
        admin_email = logged_email

        # Ensure a valid database connection
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Insert the admin and banquet relationship into OrganizeBanquet
        cursor.execute('''
            INSERT INTO OrganizeBanquet (BIN, AdminEmail)
            VALUES (?, ?)
        ''', (BIN, admin_email))
        conn.commit()
        conn.close()
        print(f"Admin {admin_email} assigned to banquet {BIN} successfully.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def retrieveAttendeeInfo():
    """
    Retrieve and display attendee information, including their registrations.
    """
    try:
        # Prompt for email and validate it
        attEmail = input("Enter attendee email: ").strip()
        if not isValidEmail(attEmail):
            print("Email address isn't valid.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Fetch attendee information
        cursor.execute("""
        SELECT Email, Password, MobileNumber, AttendeeType, Address, FirstName, LastName, Organization
        FROM Attendee
        WHERE Email = ?;
        """, (attEmail,))
        attendee = cursor.fetchone()

        # Fetch attendee's registrations
        cursor.execute("""
        SELECT * FROM Register
        WHERE AttendeeEmail = ?;
        """, (attEmail,))
        registrations = cursor.fetchall()

        # If attendee found, display details
        if attendee:
            print(f"""
------------------------------------
Attendee Found:
Email: {attendee[0]}
Name: {attendee[5]} {attendee[6]}
Type: {attendee[3]}
Organization: {attendee[7]}
Mobile Number: {attendee[2]}
Address: {attendee[4]}
------------------------------------""")

            if registrations:
                print(f"Registered Banquets for {attendee[0]}:")
                for reg in registrations:
                    binNo, _, mealID, drinkID, tableNo, price = reg
                    
                    # Fetch and display banquet information
                    cursor.execute("SELECT * FROM Banquet WHERE BIN = ?;", (binNo,))
                    banquet = cursor.fetchone()
                    if banquet:
                        print(f"""
------------------------------------
Banquet BIN: {binNo}
Name: {banquet[1]}
Date & Time: {banquet[2]}
Location: {banquet[5]}
Address: {banquet[6]}
------------------------------------""")
                    
                    # Fetch and display meal information
                    cursor.execute("SELECT * FROM Meal WHERE MealID = ? AND BIN = ?;", (mealID, binNo))
                    meal = cursor.fetchone()
                    if meal:
                        print(f"""
Meal Details:
Type: {meal[2]}
Dish Name: {meal[4]}
Price: {meal[3]}
Special Cuisine: {meal[5]}
------------------------------------""")
                    
                    # Fetch and display drink information
                    cursor.execute("SELECT * FROM Drink WHERE DrinkID = ? AND BIN = ?;", (drinkID, binNo))
                    drink = cursor.fetchone()
                    if drink:
                        print(f"""
Drink Details:
Type: {drink[2]}
Drink Name: {drink[4]}
Price: {drink[3]}
Special Cuisine: {drink[5]}
------------------------------------""")
                    
                    # Fetch and display table information
                    cursor.execute("SELECT * FROM Tables WHERE Table_Number = ? AND BIN = ?;", (tableNo, binNo))
                    table = cursor.fetchone()
                    if table:
                        print(f"""
Table Details:
Table Number: {table[1]}
Type: {table[3]}
Seat Quantity: {table[2]}
Price: {table[4]}
------------------------------------""")
            else:
                print(f"No registrations found for {attendee[0]}.")

        else:
            print("Attendee not found.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def AdminRegisterBanquet(): #should be put in admin.py
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        BIN = input("Enter Banquet ID: ").strip()
        AttendeeEmail = input("Enter AttendeeEmail: ").strip()
        
        cursor.execute("SELECT * FROM Meal WHERE BIN = ?;", (BIN,))
        meal = cursor.fetchall()
        print("\nMeal Options:")
        print("BIN\tMealID\tType\tPrice\tDishName\tSpecialCuisine")
        for row in meal:
            for attribute in row:
                print(attribute, end="\t")
            print()
        MealValidFlag = False
        MealID = None
        while(MealValidFlag == False):
            MealID = int(input("Enter MealID:").strip())
            for row in meal:
                if(row[1] == MealID):
                    MealValidFlag = True
                    break
            if(MealValidFlag == False):
                print("Invalid MealID, please try again.")
        
        cursor.execute("SELECT * FROM Drink WHERE BIN = ?;", (BIN,))
        drink = cursor.fetchall()
        print("\nDrink Options:")
        print("BIN\tDrinkID\tType\tPrice\tDrinkName\tSpecialCuisine")
        for row in drink:
            for attribute in row:
                print(attribute, end="\t")
            print()
        DrinkValidFlag = False
        DrinkID = None
        while(DrinkValidFlag == False):
            DrinkID = int(input("Enter DrinkID:").strip())
            for row in drink:
                if(row[1] == DrinkID):
                    DrinkValidFlag = True
                    break
            if(DrinkValidFlag == False):
                print("Invalid DrinkID, please try again.")
        
        cursor.execute("SELECT * FROM Tables WHERE BIN = ?;", (BIN,))
        table = cursor.fetchall()
        print("\nTable Options:")
        print("BIN\tTable_Number\tSeatQuantity\tTableType\tprice")
        for row in table:
            for attribute in row:
                print(attribute, end="\t")
            print()
        TableValidFlag = False
        Table_Number = None
        while(TableValidFlag == False):
            Table_Number = int(input("Enter Table_Number:").strip())
            for row in table:
                if(row[1] == Table_Number):
                    TableValidFlag = True
                    break
            if(TableValidFlag == False):
                print("Invalid Table_Number, please try again.")
        
        cursor.execute("SELECT price FROM Meal WHERE BIN = ? AND MealID = ?;", (BIN, MealID,))
        MealPrice = cursor.fetchone()[0]
        cursor.execute("SELECT price FROM Drink WHERE BIN = ? AND DrinkID = ?;", (BIN, DrinkID,))
        DrinkPrice = cursor.fetchone()[0]
        cursor.execute("SELECT price FROM Tables WHERE BIN = ? AND Table_Number = ?;", (BIN, Table_Number,))
        TablePrice = cursor.fetchone()[0]
        
        Total_price = MealPrice + DrinkPrice + TablePrice
        
        cursor.execute("""
        INSERT INTO Register (BIN, AttendeeEmail, MealID, DrinkID, Table_Number, Total_price)
        VALUES (?, ?, ?, ?, ?, ?);
        """, (BIN, AttendeeEmail, MealID, DrinkID, Table_Number, Total_price,))
        
        conn.commit()
        conn.close()
        
        return "Registered Banquet successfully!"
    except sqlite3.IntegrityError:
        return "Error: You are already registered in this Banquet."
    except Exception as e:
        return f"An error occurred: {e}"
    
    # Function to update meals for a banquet
def update_meals(banquet_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print("Updating meals for the banquet.")
    meal_ids = input("Enter Meal IDs to update (comma-separated): ").split(',')
    
    for meal_id in meal_ids:
        meal_id = meal_id.strip()
        print(f"\nUpdating Meal ID: {meal_id}")
        meal_type = input("Enter new meal type (leave blank to keep current): ")
        dish_name = input("Enter new dish name (leave blank to keep current): ")
        price = input("Enter new price (leave blank to keep current): ")
        special_cuisine = input("Enter new special cuisine (leave blank to keep current): ")

        update_fields = []
        params = []
        
        if meal_type:
            update_fields.append("Type = ?")
            params.append(meal_type)
        if dish_name:
            update_fields.append("DishName = ?")
            params.append(dish_name)
        if price:
            update_fields.append("Price = ?")
            params.append(float(price))
        if special_cuisine:
            update_fields.append("SpecialCuisine = ?")
            params.append(special_cuisine)
        
        if update_fields:
            params.append(meal_id)
            cursor.execute(f'''
                UPDATE Meal
                SET {', '.join(update_fields)}
                WHERE BIN = ? AND MealID = ?
            ''', (banquet_id, *params))
            conn.commit()
            print(f"Meal ID {meal_id} updated successfully.")
        else:
            print("No updates made for this meal.")
        cursor = conn.close()

# Function to update drinks for a banquet
def update_drinks(banquet_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print("Updating drinks for the banquet.")
    drink_ids = input("Enter Drink IDs to update (comma-separated): ").split(',')
    
    for drink_id in drink_ids:
        drink_id = drink_id.strip()
        print(f"\nUpdating Drink ID: {drink_id}")
        drink_type = input("Enter new drink type (leave blank to keep current): ")
        drink_name = input("Enter new drink name (leave blank to keep current): ")
        price = input("Enter new price (leave blank to keep current): ")
        special_cuisine = input("Enter new special cuisine (leave blank to keep current): ")
        
        update_fields = []
        params = []
        
        if drink_type:
            update_fields.append("Type = ?")
            params.append(drink_type)
        if drink_name:
            update_fields.append("DrinkName = ?")
            params.append(drink_name)
        if price:
            update_fields.append("Price = ?")
            params.append(float(price))
        if special_cuisine:
            update_fields.append("SpecialCuisine = ?")
            params.append(special_cuisine)
        
        if update_fields:
            params.append(drink_id)
            cursor.execute(f'''
                UPDATE Drink
                SET {', '.join(update_fields)}
                WHERE BIN = ? AND DrinkID = ?
            ''', (banquet_id, *params))
            conn.commit()
            print(f"Drink ID {drink_id} updated successfully.")
        else:
            print("No updates made for this drink.")
        cursor = conn.close()

# Function to update tables for a banquet
def update_tables(banquet_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print("Updating tables for the banquet.")
    table_numbers = input("Enter Table Numbers to update (comma-separated): ").split(',')
    
    for table_number in table_numbers:
        table_number = table_number.strip()
        print(f"\nUpdating Table Number: {table_number}")
        table_type = input("Enter new table type (leave blank to keep current): ")
        price = input("Enter new price (leave blank to keep current): ")
        
        update_fields = []
        params = []
        
        if table_type:
            update_fields.append("Type = ?")
            params.append(table_type)
        if price:
            update_fields.append("Price = ?")
            params.append(float(price))
        
        if update_fields:
            params.append(table_number)
            cursor.execute(f'''
                UPDATE SeatingTable
                SET {', '.join(update_fields)}
                WHERE BIN = ? AND TableNumber = ?
            ''', (banquet_id, *params))
            conn.commit()
            print(f"Table Number {table_number} updated successfully.")
        else:
            print("No updates made for this table.")
        cursor = conn.close()

def listBanquets():
    while(True):
        opt=int(input("\nMenu of List or Search for Banquets\nOptions:\n1. Listing Available Banquets\n2. Search Available Banquets \n0. Return to main menu\n"))
    
        if(opt==0):
            return
        elif(opt==1):
            listAvaBanquet()
        elif(opt==2):
            searchAvaBanquet()
        else:
            print("Try again!")
            

#attendee get a list of available banquets, registered or not     
def listAvaBanquet():
    try:
        t = True      
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Banquet WHERE Available = ?;", (t,))
        availables = cursor.fetchall()       
        conn.close()
        
        if availables:
            print(f"------------------------------------\nListing Available Banquets\nAvailable Banquet:")
            for available in availables:
                binNo, banqName, datetime, quota, ava, location, address, staff_fname, staff_lname = available
                print(f"BIN: {binNo}, Banquet Name: {banqName}, Date & Time: {datetime}, "
                      f"Location: {location}, Address: {address}, Quota: {quota}, "
                      f"Staff: {staff_fname} {staff_lname}")
                
        else:
            print("No available banquet now, you may check again later.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

#attendee search for a list of available banquets, registered or not         
def searchAvaBanquet():
    crit = int(input("------------------------------------\nSearch Available Banquets\nSearch options:\n1. Search by date\n2. Search by banquet name\n0. Return to Search Banquets\n"))
    whereWhat = ""
    inp = ""
    if(crit==0):
        return
    elif(crit==1):
        inp = input("Enter Date: ")
        whereWhat = "DateTime"
    elif(crit==2):
        inp = input("Enter Banquet Name: ")
        whereWhat = "Name"
    else:
        print("Try again!")
           
    try:
        t = True      
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Banquet WHERE Available = ? AND {} LIKE ?;".format(whereWhat), (t, f'%{inp}%'))
        availables = cursor.fetchall()       
        conn.close()
        
        if availables:
            print(f"------------------------------------\nAvailable Banquet Found!:")
            for available in availables:
                binNo, banqName, datetime, quota, ava, location, address = available
                print(f"BIN: {binNo}, Banquet Name: {banqName}, Date & Time: {datetime}, Location: {location}, Address: {address}, Quota: {quota}")
                
        else:
            print("No available banquet now, you may check again later.")

    except Exception as e:
        print(f"An error occurred: {e}") 
    finally:
        conn.close()


def GenerateReport():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        reportWorkbook = openpyxl.load_workbook(REPORT_PATH)
        reportWorksheet = reportWorkbook['Sheet1']

        year = input("Enter year:").strip()
        reportWorksheet["J1"] = year

        # Query for monthly banquet count
        for i in range(12):
            cursor.execute(
                "SELECT COUNT(*) FROM Banquet WHERE STRFTIME('%m-%Y', DateTime) = ?;",
                (str(i + 1).zfill(2) + "-" + year,)
            )
            reportWorksheet["K" + str(i + 1)] = cursor.fetchone()[0]  # Use fetchone() and extract the value

        # Query for previous year's banquet count
        cursor.execute(
            "SELECT COUNT(*) FROM Banquet WHERE STRFTIME('%Y', DateTime) = ?;",
            (str(int(year) - 1),)
        )
        reportWorksheet["K17"] = cursor.fetchone()[0]

        # Query for total attendee count
        cursor.execute("SELECT COUNT(*) FROM Attendee")
        TotalAttendeeCount = cursor.fetchone()[0]

        # Query for attendee types
        cursor.execute(
            "SELECT AttendeeType, COUNT(AttendeeType) FROM Attendee GROUP BY AttendeeType ORDER BY COUNT(AttendeeType) DESC;"
        )
        AttendeeType = cursor.fetchall()
        TypeCount = 0
        for i in range(min(4, len(AttendeeType))):  # Prevent index out-of-range errors
            reportWorksheet["M" + str(i + 1)] = AttendeeType[i][0]
            reportWorksheet["N" + str(i + 1)] = str(int(AttendeeType[i][1]) / TotalAttendeeCount)
            TypeCount += int(AttendeeType[i][1])

        reportWorksheet["N5"] = str(TypeCount / TotalAttendeeCount)

        # Query for monthly total price
        for i in range(12):
            cursor.execute(
                "SELECT SUM(R.Total_price) FROM Register R, Banquet B WHERE R.BIN = B.BIN AND STRFTIME('%m-%Y', B.DateTime) = ?;",
                (str(i + 1).zfill(2) + "-" + year,)
            )
            total_price = cursor.fetchone()[0]
            reportWorksheet["P" + str(i + 1)] = total_price if total_price is not None else 0  # Handle NULL values

        # Query for total price in the previous year
        cursor.execute(
            "SELECT SUM(R.Total_price) FROM Register R, Banquet B WHERE R.BIN = B.BIN AND STRFTIME('%Y', B.DateTime) = ?;",
            (str(int(year) - 1),)
        )
        total_price_last_year = cursor.fetchone()[0]
        reportWorksheet["P18"] = total_price_last_year if total_price_last_year is not None else 0

        # Query for meal counts
        cursor.execute(
            "SELECT M.DishName, COUNT(M.DishName) FROM Meal M, Register R, Banquet B "
            "WHERE R.BIN = M.BIN AND R.BIN = B.BIN AND STRFTIME('%Y', B.DateTime) = ? "
            "GROUP BY M.DishName ORDER BY COUNT(M.DishName) DESC;",
            (year,)
        )
        MealTable = cursor.fetchall()

        # Query for drink counts
        cursor.execute(
            "SELECT D.DrinkName, COUNT(D.DrinkName) FROM Drink D, Register R, Banquet B "
            "WHERE R.BIN = D.BIN AND R.BIN = B.BIN AND STRFTIME('%Y', B.DateTime) = ? "
            "GROUP BY D.DrinkName ORDER BY COUNT(D.DrinkName) DESC;",
            (year,)
        )
        DrinkTable = cursor.fetchall()

        # Write meal and drink data to the worksheet
        for i in range(min(3, len(MealTable))):  # Prevent index out-of-range errors
            reportWorksheet["J" + str(37 + i)] = MealTable[i][0]
            reportWorksheet["K" + str(37 + i)] = MealTable[i][1]

        for i in range(min(3, len(DrinkTable))):  # Prevent index out-of-range errors
            reportWorksheet["J" + str(42 + i)] = DrinkTable[i][0]
            reportWorksheet["K" + str(42 + i)] = DrinkTable[i][1]

        conn.commit()
        conn.close()

        reportWorkbook.save(year + REPORT_PATH)
        reportWorkbook.close()

        return "Report generated successfully!"
    except Exception as e:
        return f"An error occurred: {e}"

#########################################################################################
logged_email=None

print("\nWelcome to admin part!")
while(True):
    opt=int(input("\nOptions:\n1. Create account\n2. Enter account\n0. Quit\n"))
    if(opt==1):
        print("Creating acoount...")
        msg = create_admin_account()
        print(msg)
    elif(opt==2):
        print("Entering acoount...")
        msg=enterAccount()
        print(msg)
        while(logged_email!=None):
            print("\nAdmin Options:")
            print("1. Create Banquet")
            print("2. Create Meals")
            print("3. Create Drinks")
            print("4. Set up Tables")
            print("5. Retrieve Attendee Information")
            print("6. Register Attendee to Banquet")
            print("7. Update Tables")
            print("8. Update Meals")
            print("9. Update Drinks")
            print("10. List Banquets")
            print("11. Generate Report")
            print("0. Quit")
            opt = int(input("Choose an option: "))
            if(opt==0):
                logged_email=None
                print("You succesfully logged out from account.")
                break
            elif opt == 1:
                print("\nCreating a new banquet...")
                BIN = create_banquet()
                print(f"Banquet {BIN} created successfully.")
                assign_admin_to_banquet(BIN)
            
            elif opt == 2:
                BIN = input("Enter the BIN of the banquet to add meals: ").strip()
                if not bin_exists(BIN):
                    print(f"Error: BIN {BIN} does not exist. Please enter a valid BIN.")
                    continue
                print("\nAdding meals to the banquet...")
                create_meals(BIN)

            elif opt == 3:
                BIN = input("Enter the BIN of the banquet to add drinks: ").strip()
                if not bin_exists(BIN):
                    print(f"Error: BIN {BIN} does not exist. Please enter a valid BIN.")
                    continue
                print("\nAdding drinks to the banquet...")
                create_drinks(BIN)

            elif opt == 4:
                BIN = input("Enter the BIN of the banquet to set up tables: ").strip()
                if not bin_exists(BIN):
                    print(f"Error: BIN {BIN} does not exist. Please enter a valid BIN.")
                    continue
                print("\nSetting up tables for the banquet...")
                create_tables_for_banquet(BIN)

            elif opt == 5:
                print("\nRetrieving attendee information...")
                retrieveAttendeeInfo()

            elif opt == 6:
                print("\nRegister Attendee to Banquet...")
                AdminRegisterBanquet()

            elif opt == 7:
                print("\nUpdating Tables...")
                BIN = input("Enter the BIN of the banquet to update tables: ").strip()
                if not bin_exists(BIN):
                    print(f"Error: BIN {BIN} does not exist. Please enter a valid BIN.")
                    continue
                update_tables(BIN)
            elif opt == 8:
                print("\nUpdating Meals...")
                BIN = input("Enter the BIN of the banquet to update meals: ").strip()
                if not bin_exists(BIN):
                    print(f"Error: BIN {BIN} does not exist. Please enter a valid BIN.")
                    continue
                update_meals(BIN)
            elif opt == 9:
                print("\nUpdating Drinks...")
                BIN = input("Enter the BIN of the banquet to update drinks: ").strip()
                if not bin_exists(BIN):
                    print(f"Error: BIN {BIN} does not exist. Please enter a valid BIN.")
                    continue
                update_drinks(BIN)
            elif opt ==10:
                listBanquets()

            elif opt == 11:
                print(GenerateReport())
            else:
                print("Try again!")
    elif(opt==0):
        exit()
    else:
        print("Try again")

