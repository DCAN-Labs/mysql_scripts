import getpass
import mysql.connector as mysql
import os


user_prompt = "Enter a user: "
password_prompt_1 = "Enter password for {}: "
password_prompt_2 = "Confirm password for {}: "
no_match = "Passwords do not match, try again"


def get_user_name():
    while True:
        username = input(user_prompt)
        if username.isalpha():
            break
        else:
            print("Please enter a username containing only letter characters.")
    return username.lower()


def get_user_password(user='user'):
    while True:
        password1 = getpass.getpass(password_prompt_1.format(user))
        password2 = getpass.getpass(password_prompt_2.format(user))
        if password1 == password2:
            break
        else:
            print(no_match)
    return password1


def connect():
    """
    Creates a connection instance with a MySQL datebase using 
    supplied credentials via command line.
    """
    while True:
        print("Enter admin credentials to connect to DB: \n")
        user = get_user_name()
        password = get_user_password(user)
        port = input("Enter port: ")
        try:
            connection = mysql.connect(user=user, password=password, port=port)
            break
        except:
            print('err')

    return connection


def add_user(connection):
    user = get_user_name()
    password = get_user_password(user)
    cursor = connection.cursor()
    local = "CREATE USER '"+ user + "'@'localhost' IDENTIFIED BY '" + password +"';"
    from_ip = "CREATE USER '" + user + "'@'%' IDENTIFIED BY '" + password + "';"
    print("Statements to execute: \n", local, "\n", from_ip)
    cursor.execute(local, params=None, multi=False)
    cursor.execute(from_ip, params=None, multi=False)
    cursor.close()
    connection.close()


connection = connect()
add_user(connection)

