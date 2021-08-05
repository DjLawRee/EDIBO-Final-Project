import mysql.connector

db=mysql.connector.connect(user='root',password='MyNewPass',
                        host='127.0.0.1',
                        database='instaclone')
print("Conection id: ", db.connection_id)





