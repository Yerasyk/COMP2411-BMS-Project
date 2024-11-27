import sqlite3;
import re
import hashlib

DB_PATH="BMS.db"

def isValidEmail(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+$', email)

def standartName(name):
    return name.lower().capitalize()

def hashingPassw(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def create_attendee_account():
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

#########################################################################################
logged_email=None

print("\nWelcome to attendee part!")
while(True):
    opt=int(input("\nOptions:\n1. Create account\n2. Enter account\n0. Quit\n"))
    if(opt==1):
        print("Creating acoount...")
        msg = create_attendee_account()
        print(msg)
    elif(opt==2):
        print("Entering acoount...")
        msg=enterAccount()
        print(msg)
        while(logged_email!=None):
            print("\nAttendee Options:")
            print("2. List Banquets")
            print("3. Register")
            print("4. Update personal data")
            print("0. Quit")
            opt = int(input("Choose an option: "))
            if(opt==0):
                logged_email=None
                print("You succesfully logged out from account.")
                break
            elif(opt==1):
                print("Create staff")
            elif(opt==2):
                print("create a banquet")
            else:
                print("Try again!")
    elif(opt==0):
        exit()
    else:
        print("Try again")

