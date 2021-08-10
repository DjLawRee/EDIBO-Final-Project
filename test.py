from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Instaclone import db, app
import Instaclone.user_controll


email = "edas.dev@gmail.com"
test = Instaclone.user_controll.get_user_id_by_email(email)

serial = Serializer(app.config['SECRET_KEY'], 180)
token = serial.dumps({'user_id': test}).decode('utf-8')
print(token)
print(serial.loads(token))
print(serial.loads(token)["user_id"])

