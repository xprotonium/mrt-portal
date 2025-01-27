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

# connection
connection = sqlite3.connect('account.db')

# cursor
cursor = connection.cursor()

# initialize table if does not exist with username as primary key
cursor.execute("CREATE TABLE IF NOT EXISTS account (username TEXT PRIMARY KEY, password TEXT, firstName TEXT, lastName TEXT, balance INTEGER)")

# admin function
# select all data from account table
# and print all data in a table format
def admin():
    pass

# login, register, logout function - ALI
def login(): 
    pass

def register():
    pass

def logout():
    exit()

# view name - NAHIN
def view_name():
    pass

# edit name - NAHIN
def edit_name():
    pass

# edit username - NAHIN
def edit_username():
    pass

# check balance - LEE
def check_balance(username):
    pass

# reload balance - LEE
def reload_balance(username, amount):
    pass

# fare calculator - ALI
def fare_calculator():
    pass

# main function
def main():
    while True:
        cmd = input("Enter command: ")
        
        if cmd == "register":
            register()
        elif cmd == "login":
            login()
        elif cmd == "logout":
            logout()
        elif cmd == "admin":
            admin()

# call main function
if __name__ == '__main__':
    main()

# close connection
connection.close()
