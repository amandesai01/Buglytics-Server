class BuglyticsException(Exception):
    def __str__(self):
        return "Buglytics Basic Exception"

class NoProjectUnderOrganisationException(BuglyticsException):
    def __str__(self):
        return "No such project exists under given organization"

class UnidentifiedException(BuglyticsException):
    def __str__(self):
        return "Some Error. Try again or contact team."
