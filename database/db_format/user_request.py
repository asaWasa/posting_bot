from common.constants import UserRequest
from datetime import datetime


class UserRequestFormat:
    def __init__(self, data=None, id_request=None, user_id=None,
                 type_request=None, data_object=None, name=None, date_creation=None):
        self.data = dict(data)
        self.id_request = id_request
        self.user_id = user_id
        self.type_request = type_request
        self.data_object = data_object
        self.name = name
        self.date_creation = date_creation

        if data is not None:
            self.__dict__.update(data)
            return

    def __repr__(self):
        return '{}'.format(self.id_request)

    def __str__(self):
        return '{}'.format(self.id_request)

    def to_dict(self):
        result = dict()
        result[UserRequest.Id_request] = self.id_request
        result[UserRequest.User_id] = self.user_id
        result[UserRequest.Type_request] = self.type_request
        result[UserRequest.Data_object] = self.data_object
        result[UserRequest.Name] = self.name
        result[UserRequest.Date_creation] = datetime.now()
        return result
