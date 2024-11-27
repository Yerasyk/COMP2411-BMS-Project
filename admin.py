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
        while(True):
            print("\nAdmin Options:")
            print("1. Create a new Staff")
            print("2. Create Banquet")
            print("3. smth")
            print("4. Update Banquet")
            print("5. Retrieve Attendee Info")
            print("6. Generate Banquet Report")
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

