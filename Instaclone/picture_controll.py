from PIL import Image
from mysql.connector import cursor
from Instaclone import db
import base64
from multipledispatch import dispatch

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

@dispatch()
def get_all_pictures():
    cursor=db.cursor(dictionary=True)
    query="SELECT image , image_name FROM images "
    cursor.execute(query)
    images=cursor.fetchall()
    
    for image in images:
        img=image.get('image')
        decoded_img=img.decode('utf-8')
        image.update({'image':decoded_img})

    return images

@dispatch(int)
def get_all_pictures(user_id):
    cursor=db.cursor(dictionary=True)
    query=("SELECT Id, image , image_name , Likes FROM images WHERE NOT user_id = %s ORDER BY timestamp DESC ")
    cursor.execute(query,(user_id,))
    images=cursor.fetchall()
    
    for image in images:
        img=image.get('image')
        decoded_img=img.decode('utf-8')
        image.update({'image':decoded_img})

    return images

def get_top5():
    cursor=db.cursor(dictionary=True)
    query=("SELECT Id, image , image_name , Likes FROM images  ORDER BY Likes DESC LIMIT 5")
    cursor.execute(query)
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

def add_like(user_id,picture_id):
    likes=get_image_likes(picture_id)
    if likes.get("Likes")==0:
        curr_likes=1
    else :
        curr_likes=likes.get("Likes")+1
    cursor=db.cursor()
    sql=("UPDATE images SET Likes = %s WHERE Id = %s ")
    values=[curr_likes,picture_id]
    cursor.execute(sql,values)
    db.commit()
    sql_2=("INSERT INTO likes (user_id,Image_id) VALUES (%s , %s)")
    values_2=[user_id,picture_id]
    cursor.execute(sql_2,values_2)
    db.commit()
    cursor.close()

def unlike(user_id,picture_id):
    likes=get_image_likes(picture_id)
    curr_likes=likes.get("Likes")-1
    sql=("UPDATE images SET Likes = %s WHERE Id = %s ")
    values=[curr_likes,picture_id]
    cursor=db.cursor()
    cursor.execute(sql,values)
    db.commit()
    sql_2=("DELETE FROM likes WHERE user_id = %s AND Image_id= %s")
    values_2=[user_id,picture_id]
    cursor.execute(sql_2,values_2)
    db.commit()
    cursor.close()


def get_image_likes(picture_id):
    cursor=db.cursor(dictionary=True)
    sql=("SELECT Likes FROM images WHERE Id= %s")
    values=[picture_id]
    cursor.execute(sql,values)
    likes=cursor.fetchone()
    print(likes)
    cursor.close()
    return likes

def check_like(user_id,image_id):
    cursor=db.cursor(dictionary=True)
    sql=("SELECT Id FROM likes WHERE user_id= %s AND Image_Id= %s")
    values=[user_id,image_id]
    cursor.execute(sql,values)
    result=cursor.fetchone()
    print(result)
    if result :
        return True
    else : 
        return False