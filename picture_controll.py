from PIL import Image
import mysql.connector
from mysql.connector import cursor
from mysql.connector.cursor import MySQLCursor
import base64
import PIL
import io


db=mysql.connector.connect(user='root',password='MyNewPass',
                        host='127.0.0.1',
                        database='instaclone')
print("picture_controll works")
cursor=db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS `images` (`Id` int NOT NULL AUTO_INCREMENT,`user_id` int NOT NULL,`image` longblob NOT NULL,`Likes` int DEFAULT NULL,`image_name` varchar(100) NOT NULL,PRIMARY KEY (`Id`)) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;")
db.commit()
cursor.close()  

def convert_to_binary(image):
    with open(image,"rb") as file:
        binary_data = file.read()
    return binary_data

def upload_image(image , user_id, photo_name):
 
    byte_image=image.read()
    encoding = base64.b64encode(byte_image)
    query = "INSERT INTO images (user_id,image,image_name) VALUES(%s,%s,%s)"
    values=[user_id,encoding,photo_name]
    cursor = db.cursor()
    cursor.execute(query,values)
    db.commit()

def get_user_pictures(user_id):
    cursor=db.cursor(dictionary=True)
    query="SELECT image , image_name FROM images WHERE user_id= %s "
    cursor.execute(query,(user_id,))
    images=cursor.fetchall()
    
    for image in images:
        img=image.get('image')
        decoded_img=img.decode('utf-8')
        image.update({'image':decoded_img})

    return images


def test(image,image_name,user_id):
    print(image_name,user_id)
    with Image.open(image) as img:
        return img.show()