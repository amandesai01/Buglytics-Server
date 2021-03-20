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
            return jwt.encode(obj,key)
        return jwt.encode(obj, key)
    except Exception as e:
        print(e)
        return None