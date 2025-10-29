import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="ecommerce"
)


cursor = db.cursor()


cursor.execute("SHOW TABLES")
for table in cursor.fetchall():
    print(table)


cursor.close()
db.close()
