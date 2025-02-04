# *************************************************************************
# Program: mrt-account-portal.py
# Course: CSP1114 PROBLEM SOLVING AND PROGRAM DESIGN
# Lecture / Lab Section: TC4L / TL9L
# Trimester: 2430
# Names: ALI SAJULAKE ABDUL GAFUR | NAHIN BIN MONIR | LEE CHUN HUI
# IDs: 243FC245YU | 243FC245H1 | 243FC245WJ
# Emails: abdul.gafur.ali@student.mmu.edu.my | monir.nahin@gmail.com| LEE.CHUN.HUI@student.mmu.edu.my
# *************************************************************************

import sqlite3
import hashlib
from tabulate import tabulate

# connection
connection = sqlite3.connect('account.db')

# cursor
cursor = connection.cursor()

# initialize table if it does not exist with username as primary key
cursor.execute('CREATE TABLE IF NOT EXISTS account (username TEXT PRIMARY KEY, password TEXT, name TEXT, '
               'balance INTEGER)')


# admin function
# select all data from account table
# and print all data in a table format
def admin():
    cursor.execute('SELECT * FROM account')
    data = cursor.fetchall()
    # Get column names
    columns = [desc[0] for desc in cursor.description]

    # Print the table
    print(tabulate(data, headers=columns, tablefmt='grid'))


# register, login, logout function - ALI
def register(username, password, name):
    # check if the username exists in the database or not
    cursor.execute('SELECT username FROM account WHERE username = ?', (username,))
    row = cursor.fetchone()

    if row:
        print('Username is taken. Please try again')
    else:
        # hash the password for security
        password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('INSERT INTO account (username, password, name, balance) VALUES (?, ?, ?, 0)',
                       (username, password, name))
        connection.commit()
        return True
    return False


def login(username, password):
    # find the account with the username inputted and select the password from it
    cursor.execute('SELECT password FROM account WHERE username = ?', (username,))
    row = cursor.fetchone()

    # if the fetch returns a row then check if the password entered matches the hashed password in the db
    if row:
        # hash the inputted password to compare to the hashed password that is saved in the db
        password = hashlib.sha256(password.encode()).hexdigest()
        saved_password = row[0]
        if password == saved_password:
            cursor.execute('SELECT name FROM account where username = ?', (username,))
            saved_name_row = cursor.fetchone()
            saved_name = saved_name_row[0]
            print(f'Logged in successfully.\nWelcome {saved_name}!')
            return True
        else:
            print('Incorrect password.')
    else:
        print('Username does not exist.')
    return False


def logout():
    # exit the program
    exit()


# view name - NAHIN
def view_name(username):
    cursor.execute("SELECT name FROM account WHERE username = ?", (username,))
    result = cursor.fetchone()

    name = result[0]
    return name


# edit name - NAHIN
def edit_name(username, new_name):
    cursor.execute("UPDATE account SET name = ? WHERE username = ?", (new_name, username))
    connection.commit()
    print("Name changed successfully")


# edit username - NAHIN
def edit_username(username, new_username):
    cursor.execute("UPDATE account SET username = ? WHERE username = ?", (new_username, username))
    connection.commit()
    print("Username changed successfully")


# check balance - LEE
def check_balance(username):
    cursor.execute('SELECT balance FROM account WHERE username = ?', (username,))
    row = cursor.fetchone()

    if row:
        balance = row[0]
        print(f'Your account balance is: RM{balance}')
    else:
        print("Username does not exist.")


# reload balance - LEE
def reload_balance(username, amount):
    cursor.execute('UPDATE account SET balance = balance + ? WHERE username = ?', (amount, username))
    connection.commit()
    print(f'Your balance has been reloaded by RM{amount}.')
    if amount > 50:
        print("Wow! That's a significant top-up! You're on your way to achieving your goals!")
    elif amount > 0:
        print("Great! Every little bit helps. Keep it up!")
    else:
        print("It seems like you didn't add any funds. Consider reloading your balance soon!")


# fare calculator - ALI
def fare_calculator():
    stations = ['PUTRAJAYA SENTRAL',
                'CYBERJAYA CITY CENTRE',
                'CYBERJAYA UTARA',
                '16 SIERRA',
                'PUTRA PERMAI',
                'TAMAN EQUINE',
                'UPM',
                'SERDANG JAYA',
                'CHAN SOW LIN',
                'TUN RAZAK EXCHANGE (TRX)',
                'AMPANG PARK',
                'KLCC']

    # print all the stations available
    print('Stations available: ')
    for i, station in enumerate(stations, start=1):
        print(f'{i}. {station}')

    # prompt the user for the starting station and destination station
    while True:
        starting = input('Enter starting station: ').upper().strip()
        destination = input('Enter destination: ').upper().strip()

        # check if the entered stations exist on the stations list
        if starting not in stations or destination not in stations:
            print('Invalid station name entered. Please check if the station exists on the list.')
        else:
            break

    # calculate the fare
    # to do this, index of each station is taken and the absolute value is calculated to imitate distance
    starting_index = stations.index(starting)
    destination_index = stations.index(destination)
    number_of_stations = abs(destination_index - starting_index)
    fare = 2 * number_of_stations
    print(f'The fare from {starting} station -> {destination} station is RM{fare}')


# main function - ALI, NAHIN, LEE
def main():
    print('WELCOME TO THE MRT ACCOUNT PORTAL')
    # check if the user is logged in or not, some functions are meant to be executed only if the user is logged in.
    # another reason for this check is that if the user is already logged in, do not allow the user to log in again.
    logged_in = False
    username = None
    while True:
        cmd = input('type "help" for list of commands.\n>> ').strip().lower()

        # check for the different commands
        if cmd == 'register':
            if logged_in:
                print('Cannot register, already logged in. Please logout if you want to make another account')
            else:
                while True:
                    username = input('Enter username: ')
                    while True:
                        password = input('Enter password: ')
                        confirm_password = input('Confirm password: ')
                        if confirm_password == password:
                            break
                        else:
                            print('Passwords do not match, please try again:')

                    name = input('Enter name: ')
                    if register(username, password, name):
                        print('Account registered successfully.\nYou can log in to your account now.')
                        break
                    else:
                        print('Registration failed. Please try again.')
        elif cmd == 'login':
            # check if the user is already logged in or not
            if logged_in:
                print('Already logged in.')
            else:
                # prompt for username and password
                username = input('Enter username: ')
                password = input('Enter password: ')
                # if the login function returns true, change the logged in status to true as well
                if login(username, password):
                    logged_in = True
                    cursor.execute("SELECT username FROM account WHERE username = ?", (username,))
                    result = cursor.fetchone()
                    username = result[0]
                else:
                    logged_in = False
        elif cmd == 'logout':
            logout()
        elif cmd == 'view name':
            if not logged_in:
                print('You are not logged in.')
            else:
                print(view_name(username))
        elif cmd == 'edit name':
            if not logged_in:
                print('You are not logged in.')
            else:
                username = username
                new_name = input("Enter new name: ")
                edit_name(username, new_name)
        elif cmd == 'edit username':
            if not logged_in:
                print('You are not logged in.')
            else:
                username = username
                new_username = input("Enter a new username: ")
                edit_username(username, new_username)
                username = new_username
        elif cmd == 'check balance':
            if not logged_in:
                print('You are not logged in.')
            else:
                username = username
                check_balance(username)
        elif cmd == 'reload balance':
            if not logged_in:
                print("You are not logged in.")
            else:
                username = username
                while True:
                    amount = input("Enter amount\nType cancel to cancel process\n>> ").strip()
                    # check if the input entered is digit or not
                    # if it is, convert it to an integer
                    if amount.isdigit():
                        amount = int(amount)
                        reload_balance(username, amount)
                        break
                    elif amount.lower() == "cancel":
                        break
                    else:
                        print("Invalid amount entered. Please try again.")
        elif cmd == 'fare calculator' or cmd == 'fare' or cmd == 'fare calc':
            if not logged_in:
                print('You are not logged in.')
            else:
                fare_calculator()
        elif cmd == 'admin':
            admin()
        elif cmd == 'help':
            print(
                'register\nlogin\nlogout\nview name\nedit name\nedit username\ncheck balance\nreload balance\nfare calculator')
        else:
            print('Invalid command')


# call main function
if __name__ == '__main__':
    main()

# close connection
connection.close()
