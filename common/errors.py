class NoValidToken(Exception):
    def __init__(self, text=None):
        self.text = text


class BadImage(Exception):
    def __init__(self, text=None):
        self.text = text


class EmptyRequest(Exception):
    def __init__(self, text=None):
        self.text = text


class RequestIsNone(Exception):
    def __init__(self, text=None):
        self.text = text


class BadCaption(Exception):
    def __init__(self, text=None):
        self.text = text


class BadRequest(Exception):
    def __init__(self, text=None):
        self.text = text


class BadNameHandler(Exception):
    def __init__(self, text=None):
        self.text = text


class BusinessIdError(Exception):
    def __init__(self, text=None):
        self.text = text


class UserTokenError(Exception):
    def __init__(self, text=None):
        self.text = text


class UserCaptionError(Exception):
    def __init__(self, text=None):
        self.text = text


class UserGoBack(Exception):
    def __init__(self, text=None):
        self.text = text