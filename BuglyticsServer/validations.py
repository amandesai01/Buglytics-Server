import re

from BuglyticsServer.exceptions import SecretInvalidException

def validate_secret(user_password) :
    regex = "^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8,32}$"
    if not (re.search(regex, user_password)):
        raise SecretInvalidException