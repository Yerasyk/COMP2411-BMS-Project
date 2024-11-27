import subprocess

while(True):
    print("\nSelect option as you want to enter or 0 to exit:\n1. Administrator\n2. Attendee")
    opt=int(input("Choose: "))
    if(opt==1):
        subprocess.run(["python", "admin.py"])
    elif(opt == 2):
        subprocess.run(["python", "attendee.py"])
    elif(opt == 0):
        exit()
    else:
        print("Try again!")