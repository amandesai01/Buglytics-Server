import jwt
import datetime

def get_object_from_token(token, key):
    try:
        return jwt.decode(token, key, algorithms=['HS256'])
    except jwt.DecodeError as e:
        print(e)
        return None

def get_token_from_object(obj, key, time=None):
    try:
        if time:
            obj['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=time)
            return jwt.encode(obj,key).decode("utf-8")
        return jwt.encode(obj, key).decode("utf-8")
    except Exception as e:
        print(e)
        return None