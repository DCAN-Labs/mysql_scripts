
import getpass
import mysql.connector as mysql
import os
import subprocess
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
    """
    Gets and verifies entered password for a new user.
    :param user: user who a password is being created for.
    """
    while True:
        password1 = getpass.getpass(password_prompt_1.format(user))
        password2 = getpass.getpass(password_prompt_2.format(user))
        if password1 == password2:
            break
        else:
            print(no_match)
    return password1


def backup_db(output_file=None):
	"""
	Create backup file containing all data stored in mysql database.
	:param output_file: Path to backup file which will be created.
	"""
	# If no output filepath is given, use user's home directory as default
	if not output_file:
		output_file = "~/mysql_database_backup.sql"

	# Run call to create database backup 
	cmd = "mysqldump --all_databases -p > " + output_file
	subprocess.run(cmd, shell=True)


def connect():
    """
    Creates a connection instance with a MySQL datebase using 
    supplied credentials via command line.
    """
    while True:
        print("Enter admin credentials to connect to DB: \n")
        user = get_user_name()
        password = getpass.getpass(password_prompt_1.format(user))
        port = input("Enter port (press enter to use default 3306): ")
        if port is '':
            port = 3306
        try:
            connection = mysql.connect(user=user, password=password, port=port)
            break
        except mysql.Error as err:
            print("Something went wrong with connection: {}".format(err))

    return connection


def all_query(connection, query):
    """
    Makes a simple query on the database and returns the output of that result.
    :param connection: a MySQL connector datatype pointing to a DB
    :param query: A SQL command to execute on the database.
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    return cursor


def print_users(connection, visible=True):
    """
    Prints to console all users in the database by default, if visible
    is True console print is disabled and this function merely returns
    a sorted list of all users
    :param connection: a MySQL connector datatype pointing to a DB
    :param visible: Boolean to turn on or off print statements to console.
    """
    query = "select user, host from mysql.user;"
    user_dict = all_query(connection, query)
    user_list = []
    for row in user_dict:
        user_list.append("{user}@{host}".format(**row))
    user_list.sort()
    if visible is True:
        print("Current user list: \n")
        for each in user_list:
            print(each)
        print('\n')
    return user_list


def add_user(connection):
    """
    Adds a user to a database located at the connection object passed
    to it.
    :param connection: a MySQL connector datatype pointing to a DB
    """
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


def del_user(connection, user):
    """
    Creates a delete command given a connection and a user to delete.
    :param connection: a MySQL connector datatype pointing to a DB
    :param user: A string containing a username to be deleted
    """ 

    if user.lower() != "root":
        drop_these = []
        drop_these.append("DROP USER " + user + "@localhost;")
        drop_these.append("DROP USER " + user + ";")
        cursor = connection.cursor()
        for each in drop_these:
            try:
                cursor.execute(each, params=None, multi=False)
                print("Successfully applied: {}".format(each))
            except mysql.Error as err:
                print("Unable to remove user: {} \n {}".format(user, err))
    else:
        print("Please Enter a valid user to remove.")
    cursor.close()


def remove_user(connection):
    """
    Removes a USER based on keyboard input using the del_user method.
    :param connection: a MySQL connector datatype pointing to a DB
    """
    print("Current Users on server: \n")
    print_users(connection)
    once = input("Enter the name of the user to be removed: ")
    twice = input("Re-enter the user's name to confirm :     ")
    if once == twice and once.lower() != 'root':
        del_user(connection, once)
    elif once.lower() == twice.lower() == 'root':
        print("Don't delete the root user")
    else:
        print("No user selected for deletion.")


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


def grant_privileges_table(user, permissions, database, tables):
    where = ('localhost', '%')
    for both in where:
        for table in tables:
            statement = "GRANT {} ON {}.{} TO '{}'@'{}';"\
                    .format(permissions, database, table, user, both)
            yield statement
    
     


def create_database(connection):
    pass


def destory_database(connection):
    pass

if __name__ == "__main__":
    connection = connect()
    print_users(connection)
