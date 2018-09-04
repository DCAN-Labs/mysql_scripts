import getpass
import mysql.connector as mysql
import os
import yaml

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
        except mysql.Error as err:
            print("Something went wrong with connection: {}".format(err))

    return connection


def all_query(connection, query):
    """
    Makes a simple query on the database and returns the output of that result.
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    return cursor


def print_users(connection):
    query = "select user, host from mysql.user;"
    user_dict = all_query(connection, query)
    user_list = []
    for row in user_dict:
        user_list.append("{user}@{host}".format(**row))
    user_list.sort()
    print("Current user list: \n")
    for each in user_list:
        print(each)
    print('\n')


def add_user(connection):
    user = get_user_name()
    password = get_user_password(user)
    cursor = connection.cursor()
    local = "CREATE USER '"+ user + "'@'localhost' IDENTIFIED BY '" + password +"';"
    from_ip = "CREATE USER '" + user + "'@'%' IDENTIFIED BY '" + password + "';"
    try:
        cursor.execute(local, params=None, multi=False)
        cursor.execute(from_ip, params=None, multi=False)
    except mysql.Error as err:
        print("Something went wrong: {}".format(err))
    cursor.close()
    connection.close()


def load_yaml(file_name):
    try:
        with open(file_name, 'r') as stream:
            yaml_doc = yaml.load(stream)
            return yaml_doc
    except FileNotFoundError as err:
        print("Encountered {} , check to see if file path exists".format(err))
        return None
    except yaml.parser.ParserError as err:
        print("Bad yaml: {}".format(err))
        return None


if __name__ == "__main__":
    connection = connect()
    print_users(connection)
    add_user(connection)

