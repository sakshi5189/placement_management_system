import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="placement_db",
    port=3306
)

cursor = conn.cursor(dictionary=True)