import mysql.connector
from mysql.connector import Error, connect

def create_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def connect_to_database(connection):
    cursor = connection.cursor()
    cursor.execute("use loginInfo")
    return cursor

def getLoginInfo(database_name):
    connection = create_connection("127.0.0.1", "root", "@HoangAnkin123")
    cursor = connect_to_database(connection)
    cursor.execute("select * from "+database_name)
    data = cursor.fetchall()
    connection.close()
    return data

def add_new_user(username,password,database_name):
    connection = create_connection("127.0.0.1", "root", "@HoangAnkin123")
    cursor = connect_to_database(connection)
    cursor.execute("insert into "+ database_name + " (username,password) values ('"+username+"','"+password+"');")
    connection.commit()
    connection.close()
    return

    