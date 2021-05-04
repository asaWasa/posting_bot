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
