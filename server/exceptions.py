class BuglyticsException(Exception):
    def __str__(self):
        return "Buglytics Basic Exception"

class NoProjectUnderOrganisationException(BuglyticsException):
    def __str__(self):
        return "No such project exists under given organization"

class UnidentifiedException(BuglyticsException):
    def __str__(self):
        return "Some Error. Try again or contact team."

class SecretInvalidException(BuglyticsException):
    def __str__(self):
        return "Password submitted was invalid. It must contain [0-9], [a-z], [A-Z], atleast one special character, " \
               "length between 8 to 32. "

class PasswordMismatchException(BuglyticsException):
    def __str__(self):
        return "Given password not matching with actual password."

class EmailAlreadyExistsException(BuglyticsException):
    def __str__(self):
        return "This email is already registered."

class ProjectNotFoundException(BuglyticsException):
    def __str__(self):
        return "No such project found under this organization."