
"""
# Premierement
# Installer mysql dans votre pc
# pip install mysql
# pip install mysql-connector
# pip install mysql-connector-python
"""
import mysql.connector

dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
)


cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE basedigiblood")

print("Bien Connecté!")