# Banquet Management System (BMS)

A Python-based command-line application for managing banquet events, attendees, and administrators. This system allows for user registration, banquet management, and attendance tracking using SQLite.

**Note**: This is a group project for COMP2411 (Database Systems) at PolyU.

## Features

- **Administrator Panel**: Create admin accounts, manage banquets, and view reports
- **Attendee Portal**: Register as an attendee, browse available banquets, and make reservations
- **Database Management**: SQLite-based persistent data storage with automated schema creation
- **Input Validation**: Email, name, and password validation with hashing for security
- **Reporting**: Excel export functionality for banquet reports

## Project Structure

```
COMP2411-BMS-Project/
├── main.py              # Entry point with user role selection
├── admin.py             # Administrator functionalities
├── attendee.py          # Attendee functionalities
├── db_creation.py       # Database schema initialization
├── observe.py           # Database inspection utility
├── README.md            # This file
└── .gitignore          # Git ignore rules
```

## Files Overview

### `main.py`
Entry point that presents a menu for users to choose between:
1. Administrator login/operations
2. Attendee login/operations
3. Exit

### `admin.py`
Handles administrator operations including:
- Admin account creation and login
- Banquet creation and management
- Viewing attendee lists for banquets
- Generating reports in Excel format
- Password hashing with SHA-256

### `attendee.py`
Manages attendee operations including:
- Account creation and registration
- Login authentication
- Viewing available banquets
- Making banquet reservations
- Viewing booking history

### `db_creation.py`
Initializes the SQLite database with the following tables:
- **Administrator**: Stores admin accounts with email, name, and hashed password
- **Attendee**: Stores attendee information (email, contact, organization, etc.)
- **Banquet**: Stores banquet details (name, date, location, quota, staff info)
- **Meal**: Stores meal options for banquets
- **Booking**: Tracks attendee reservations for banquets

### `observe.py`
Utility script to inspect the database contents, displaying all tables and their data.

## Requirements

- Python 3.x
- SQLite3 (included with Python)
- openpyxl (for Excel report generation)

## Installation

1. Initialize the database:
```bash
python db_creation.py
```

## Usage

### Start the Application
```bash
python main.py
```

### View Database Contents
```bash
python observe.py
```

## Database Schema

### Administrator Table
- `Email` (PRIMARY KEY): Unique email address
- `Name`: Administrator name
- `Password`: SHA-256 hashed password

### Attendee Table
- `Email` (PRIMARY KEY): Unique email address
- `Password`: SHA-256 hashed password
- `MobileNumber`: 8-digit phone number
- `AttendeeType`: Type of attendee (staff, student, alumni, guest)
- `Address`: Physical address
- `FirstName`: First name
- `LastName`: Last name
- `Organization`: Affiliated organization

### Banquet Table
- `BIN` (PRIMARY KEY): Banquet ID (18 characters)
- `Name`: Banquet name
- `DateTime`: Event date and time
- `Quota`: Maximum attendees
- `Available`: Availability status
- `Location`: Venue name
- `Address`: Venue address
- `Staff_FName`: Staff first name
- `Staff_LName`: Staff last name

## Security Features

- Passwords are hashed using SHA-256 algorithm
- Email validation using regex patterns
- SQL constraints for data integrity
- Foreign key enforcement in SQLite

## Notes

- This project is designed as a coursework for COMP2411 (Database Systems)
- The system uses SQLite for lightweight, serverless database operations
- All user input is validated before database insertion
- Excel reports are generated with `BMSReport.xlsx` filename