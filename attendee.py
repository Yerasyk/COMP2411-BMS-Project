import sqlite3;
import re
import hashlib

DB_PATH="BMS.db"

def isValidEmail(email):
    return re.match(r'^.+@.+\..+$', email)

def standartName(name):
    return name.lower().capitalize()

def hashingPassw(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def createAttendeeAccount():
    try:
        #Handling inputs
        email=input("Write your email: ").strip()
        if(isValidEmail(email)==None):
            return "Email address isn't valid."
        
        first_name = input("Write your first name: ").strip()
        first_name = standartName(first_name)

        last_name = input("Write your last name: ").strip()
        last_name = standartName(last_name)

        password= input("Write your password: ").strip()
        hashed_password=hashingPassw(password)

        address = input("Write your address: ").strip()
        mobile_number = input("Write your mobile number (8 digits): ").strip()
        if not (mobile_number.isdigit() and len(mobile_number) == 8):
            return "Mobile number must be 8 digits."
        
        attendee_type = input("Write your attendee type (e.g., staff, student, alumni, guest): ").strip().capitalize()
        organization = input("Write your affiliated organization (e.g., PolyU, SPEED, HKCC, Others): ").strip()


        #Inserting into table
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO Attendee (Email, Password, MobileNumber, AttendeeType, Address, FirstName, LastName, Organization)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (email, hashed_password, mobile_number, attendee_type, address, first_name, last_name, organization))

        conn.commit()
        conn.close()

        return "Attendee account created successfully!"
    except sqlite3.IntegrityError:
        return "Error: Attendee with this email already exists."
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
        SELECT Email, FirstName FROM Attendee
        WHERE Email = ? AND Password = ?;
        """, (email, hashed_password))

        attendee = cursor.fetchone()

        conn.close()

        if attendee:
            logged_email=attendee[0]
            return f"Login successful! Welcome, {attendee[1]} (Email: {attendee[0]})."
        else:
            return "Error: Invalid email or password."

    except Exception as e:
        return f"An error occurred: {e}"

def showPersonalData():
    try:
        global logged_email
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Attendee WHERE Email = ?;", (logged_email,))
        attendee = cursor.fetchone()

        print("\nCurrent Data:")
        column_names = ["Email", "Password", "MobileNumber", "AttendeeType", "Address", "FirstName", "LastName", "Organization"]
        for i in range(len(column_names)):  
            print(f"{column_names[i]}: {attendee[i]}")
       
        conn.close()

        return attendee

    except Exception as e:
        return f"An error occurred: {e}"

def updatePersonalData():
    try:
        global logged_email
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        attendee=showPersonalData()

        print("\nEnter new values (leave blank to keep the current value):")
        new_email= input("New Email: ").strip()
        if new_email:
            if(isValidEmail(new_email)==None):
                return "Email address isn't valid."
        else:
            new_email=attendee[0]

        new_password = input("New Password: ").strip()
        if new_password:
            new_hashed_password=hashingPassw(new_password)
        else: 
            new_hashed_password=attendee[1]

        new_mobile_number = input("New Mobile Number (8 digits): ").strip()
        if new_mobile_number:
            if not (new_mobile_number.isdigit() and len(new_mobile_number) == 8):
                return "Mobile number must be 8 digits."
        else:
            new_mobile_number =  attendee[2]

        new_attendee_type = input("New Attendee Type (e.g., staff, student, alumni, guest): ").strip()
        if new_attendee_type==False:
            new_attendee_type = attendee[3]

        new_address = input("New Address: ").strip()
        if new_address == False: 
            new_address = attendee[4]

        new_first_name = input("New First Name: ").strip()
        if new_first_name:
            new_first_name = standartName(new_first_name) 
        else: 
            new_first_name = attendee[5]

        new_last_name = input("New Last Name: ").strip()
        if new_last_name:
            new_last_name = standartName(new_last_name) 
        else: 
            new_last_name = attendee[6]

        new_organization = input("New Organization: ").strip()
        if new_organization==False:
            new_organization = attendee[7]

        # Update attendee data
        cursor.execute("""
        UPDATE Attendee
        SET Email=?, Password = ?, MobileNumber = ?, AttendeeType = ?, Address = ?, FirstName = ?, LastName = ?, Organization = ?
        WHERE Email = ?;
        """, (new_email, new_hashed_password, new_mobile_number, new_attendee_type, new_address, new_first_name, new_last_name, new_organization, logged_email))

        conn.commit()
        conn.close()

        logged_email=new_email
        return "Your data has been updated successfully!"

    except Exception as e:
        return f"An error occurred: {e}"

def listBanquets():
    while(True):
        opt=int(input("\nMenu of List or Search for Banquets\nOptions:\n1. Listing Registered Banquets\n2. Searching Registered Banquets\n3. Listing Available Banquets\n4. Search Available Banquets\n0. Return to main menu\n"))
    
        if(opt==0):
            return
        elif(opt==1):
            listReqBanquet()
        elif(opt==2):
            searchReqBanquet()
        elif(opt==3):
            listAvaBanquet()
        elif(opt==4):
            searchAvaBanquet()
        else:
            print("Try again!")
            
#attendee get the list of registered banquets             
def listReqBanquet():
    try:
        global logged_email       
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Register WHERE AttendeeEmail = ?;", (logged_email,))
        registers = cursor.fetchall()
        
        if registers:
            print(f"------------------------------------\nListing Registered Banquets\nRegisted Banquet of {logged_email}:")
            for register in registers:
                binNo, attEmail, mealID, drinkID, tableNo, price = register
                print(f"BIN: {binNo}, MealID: {mealID}, DrinkID: {drinkID}, Total Price: {price}")
                
                cursor.execute("SELECT * FROM Banquet WHERE BIN = ?;", (binNo,))
                banquet = cursor.fetchone()
                #for print of banquet info here, I haven't include the contact_first_name and contact_last_name.
                # And the index of banquet[?] might need to change here
                print(f"Banquet Name: {banquet[1]}, Date & Time: {banquet[2]}, Location: {banquet[5]}, Address: {banquet[6]}")
                
                cursor.execute("SELECT * FROM Meal WHERE MealID = ?;", (mealID,))
                meal = cursor.fetchone()
                print(f"Meal type: {meal[2]}, Dish Name: {meal[4]}, Price: {meal[3]}, SpecialCuisine: {meal[5]}")
                
                cursor.execute("SELECT * FROM Drink WHERE DrinkID = ?;", (drinkID,))
                drink = cursor.fetchone()
                print(f"Drink type: {drink[2]}, Drink Name: {drink[4]}, Price: {drink[3]}, SpecialCuisine: {drink[5]}")
                
                cursor.execute("SELECT * FROM Tables WHERE Table_Number = ?;", (tableNo,))
                table = cursor.fetchone()
                print(f"Table Number: {tableNo}, Table type: {table[3]}, Seat Quantity: {table[2]}, Price: {table[4]}")               
        else:
            print("No registrations found.")
        conn.close()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

#attendee search for list of registered banquets           
def searchReqBanquet():
    crit = int(input("------------------------------------\nSearching Registered Banquets\nSearch options:\n1. Search by date\n2. Search by banquet name\n0. Return to Search Banquets\n"))
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
        global logged_email       
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        #for search using date, 'WHERE Datetime LIKE ???' is used.
        cursor.execute("SELECT R.BIN, R.MealID, R.DrinkID, R.Table_Number, R.Total_price FROM Banquet B, Register R WHERE R.AttendeeEmail = ? AND B.{} LIKE ? GROUP BY R.BIN;".format(whereWhat), (logged_email, f'%{inp}%'))
        registers = cursor.fetchall()
        
        if registers:
            print(f"------------------------------------\nRegisted Banquet of {logged_email} Found!:")
            for register in registers:
                binNo, mealID, drinkID, tableNo, price = register
                print(f"BIN: {binNo}, MealID: {mealID}, DrinkID: {drinkID}, Total Price: {price}")
                
                cursor.execute("SELECT * FROM Banquet WHERE BIN = ?;", (binNo,))
                banquet = cursor.fetchone()
                #for print of banquet info here, I haven't include the contact_first_name and contact_last_name.
                # And the index of banquet[?] might need to change here
                print(f"Banquet Name: {banquet[1]}, Date & Time: {banquet[2]}, Location: {banquet[5]}, Address: {banquet[6]}")
                
                cursor.execute("SELECT * FROM Meal WHERE MealID = ?;", (mealID,))
                meal = cursor.fetchone()
                print(f"Meal type: {meal[2]}, Dish Name: {meal[4]}, Price: {meal[3]}, SpecialCuisine: {meal[5]}")
                
                cursor.execute("SELECT * FROM Drink WHERE DrinkID = ?;", (drinkID,))
                drink = cursor.fetchone()
                print(f"Drink type: {drink[2]}, Drink Name: {drink[4]}, Price: {drink[3]}, SpecialCuisine: {drink[5]}")
                
                cursor.execute("SELECT * FROM Tables WHERE Table_Number = ?;", (tableNo,))
                table = cursor.fetchone()
                print(f"Table Number: {tableNo}, Table type: {table[3]}, Seat Quantity: {table[2]}, Price: {table[4]}")
                
                #conn.close()
        else:
            print("No registrations found.")
        conn.close()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


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


def AttendeeRegisterBanquet(): #should be put in attendee.py
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        BIN = input("Enter Banquet ID:").strip()
        
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
        
        cursor.execute("SELECT Price FROM Meal WHERE BIN = ? AND MealID = ?;", (BIN, MealID,))
        MealPrice = cursor.fetchone()[0]
        cursor.execute("SELECT Price FROM Drink WHERE BIN = ? AND DrinkID = ?;", (BIN, DrinkID,))
        DrinkPrice = cursor.fetchone()[0]
        cursor.execute("SELECT Price FROM Tables WHERE BIN = ? AND Table_Number = ?;", (BIN, Table_Number,))
        cursor.execute("SELECT Price FROM Tables WHERE BIN = ? AND Table_Number = ?;", (BIN, Table_Number,))
        TablePrice = cursor.fetchone()[0]
        
        Total_price = MealPrice + DrinkPrice + TablePrice
        
        cursor.execute("""
        INSERT INTO Register (BIN, AttendeeEmail, MealID, DrinkID, Table_Number, Total_price)
        VALUES (?, ?, ?, ?, ?, ?);
        """, (BIN, logged_email, MealID, DrinkID, Table_Number, Total_price))
        
        conn.commit()
        conn.close()
        
        return "Registered Banquet successfully!"
    except sqlite3.IntegrityError:
        return "Error: You are already registered in this Banquet."
    except Exception as e:
        return f"An error occurred: {e}"
#########################################################################################
logged_email=None

print("\nWelcome to attendee part!")
while(True):
    opt=int(input("\nOptions:\n1. Create account\n2. Enter account\n0. Quit\n"))
    if(opt==1):
        print("Creating acoount...")
        msg = createAttendeeAccount()
        print(msg)
    elif(opt==2):
        print("Entering acoount...")
        msg=enterAccount()
        print(msg)
        while(logged_email!=None):
            print("\nAttendee Options:")
            print("1. List Banquets")
            print("2. Register")
            print("3. Update personal data")
            print("4. Show personal data")
            print("0. Quit")
            opt = int(input("Choose an option: "))
            if(opt==0):
                logged_email=None
                print("You succesfully logged out from account.")
                break
            elif(opt==1):
                print("Listing Banquets...")
                listBanquets()
            elif(opt==2):
                print("Registering...")
                AttendeeRegisterBanquet()
            elif(opt==3):
                print("Updating personal info...")
                msg=updatePersonalData()
                print(msg)
            elif(opt==4):
                print("Showing personal info...")
                showPersonalData()
            else:
                print("Try again!")
    elif(opt==0):
        exit()
    else:
        print("Try again")

