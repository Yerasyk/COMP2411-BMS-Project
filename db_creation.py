import sqlite3

conn = sqlite3.connect('BMS.db')

cursor = conn.cursor()

# Enable foreign key enforcement (important for SQLite)
cursor.execute("PRAGMA foreign_keys = ON;")

# Create Administrator Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Administrator (
    Email VARCHAR(320) PRIMARY KEY CHECK(Email LIKE '%_@%_.%_'),
    Name VARCHAR(255) NOT NULL CHECK (Name GLOB '[a-zA-Z ]*'),
    Password CHAR(64) NOT NULL
);
""")

# Create Attendee Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Attendee (
    Email VARCHAR(320) PRIMARY KEY CHECK(Email LIKE '%_@%_.%_'),
    Password CHAR(64) NOT NULL,
    MobileNumber NUMERIC(8,0),
    AttendeeType VARCHAR(255),
    Address TEXT NOT NULL,
    FirstName VARCHAR(255) NOT NULL CHECK (FirstName GLOB '[a-zA-Z ]*'),
    LastName VARCHAR(255) NOT NULL CHECK (LastName GLOB '[a-zA-Z ]*'),
    Organization VARCHAR(255) NOT NULL
);
""")

# Create Banquet Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Banquet (
    BIN CHAR(18) PRIMARY KEY, 
    Name TEXT NOT NULL,
    DateTime DATETIME NOT NULL,
    Quota INTEGER NOT NULL,
    Available BOOLEAN NOT NULL,
    Location TEXT NOT NULL,
    Address TEXT NOT NULL,
    Staff_FName VARCHAR(255) NOT NULL CHECK (Staff_FName GLOB '[a-zA-Z ]*'),
    Staff_LName VARCHAR(255) NOT NULL CHECK (Staff_LName GLOB '[a-zA-Z ]*')
);
""")

# Create Meal Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Meal (
    BIN CHAR(18) NOT NULL,
    MealID INTEGER NOT NULL,
    Type VARCHAR(255) NOT NULL,
    Price DECIMAL(5,2) NOT NULL,
    DishName TEXT NOT NULL,
    SpecialCuisine TEXT,
    PRIMARY KEY (BIN, MealID),
    FOREIGN KEY (BIN) REFERENCES Banquet(BIN) ON DELETE CASCADE
);
""")

# Create Drink Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Drink (
    BIN CHAR(18) NOT NULL,
    DrinkID INTEGER NOT NULL,
    Type VARCHAR(255) NOT NULL,
    Price DECIMAL(5,2) NOT NULL, 
    DrinkName VARCHAR(255) NOT NULL,
    SpecialCuisine TEXT,
    PRIMARY KEY (BIN, DrinkID),
    FOREIGN KEY (BIN) REFERENCES Banquet(BIN) ON DELETE CASCADE
);
""")

# Create Tables Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Tables (
    BIN CHAR(18) NOT NULL,
    Table_Number INTEGER NOT NULL,
    SeatQuantity INTEGER NOT NULL,
    TableType VARCHAR(255) NOT NULL,
    Price DECIMAL(5,2) NOT NULL,
    PRIMARY KEY (BIN, Table_Number),
    FOREIGN KEY (BIN) REFERENCES Banquet(BIN) ON DELETE CASCADE
);
""")

# Create Register Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Register (
    BIN CHAR(18) NOT NULL,
    AttendeeEmail VARCHAR(320) NOT NULL,
    MealID INTEGER NOT NULL,
    DrinkID INTEGER NOT NULL,
    Table_Number INTEGER NOT NULL,
    Total_price DECIMAL(5,2) NOT NULL,
    PRIMARY KEY (BIN, AttendeeEmail),
    FOREIGN KEY (BIN) REFERENCES Banquet(BIN) ON DELETE CASCADE, 
    FOREIGN KEY (AttendeeEmail) REFERENCES Attendee(Email) ON DELETE CASCADE,
    FOREIGN KEY (BIN, MealID) REFERENCES Meal(BIN, MealID),
    FOREIGN KEY (BIN, DrinkID) REFERENCES Drink(BIN, DrinkID),
    FOREIGN KEY (BIN, Table_Number) REFERENCES Tables(BIN, Table_Number)
);
""")

# Create OrganizeBanquet Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS OrganizeBanquet (
    AdminEmail VARCHAR(320) NOT NULL,
    BIN CHAR(18) NOT NULL,
    PRIMARY KEY (AdminEmail, BIN),
    FOREIGN KEY (AdminEmail) REFERENCES Administrator(Email),
    FOREIGN KEY (BIN) REFERENCES Banquet(BIN) ON DELETE CASCADE
);
""")

conn.commit()
conn.close()