from common.constants import UserData, Rights, NONE


class UserFormat:
    def __init__(self, data):
        self.data = dict(data)

    def to_dict(self):
        result = dict()
        result[UserData.Time] = 0
        result[UserData.Id] = self.data[UserData.Id]
        result[UserData.Is_bot] = self.data[UserData.Is_bot]
        result[UserData.First_name] = self.data[UserData.First_name]
        result[UserData.Username] = self.data[UserData.Username]
        result[UserData.Language_code] = self.data[UserData.Language_code]
        result[UserData.Admin_rule] = Rights.User
        result[UserData.Social_net] = dict()

        return result
