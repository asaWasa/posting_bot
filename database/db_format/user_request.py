from common.constants import UserRequest
from datetime import datetime


class UserRequestFormat:
    def __init__(self, data):
        self.data = dict(data)

    def to_dict(self):
        result = dict()
        result[UserRequest.Id_request] = self.data[UserRequest.Id_request]
        result[UserRequest.User_id] = self.data[UserRequest.User_id]
        result[UserRequest.Type_request] = self.data[UserRequest.Type_request]
        result[UserRequest.Data] = self.data[UserRequest.Data]
        result[UserRequest.Date_creation] = datetime.now()
        return result
