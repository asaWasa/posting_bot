from common.constants import USER, RIGHT, NONE


class USER_FORMAT:
    def __init__(self, data):
        self.data = dict(data)

    def to_dict(self):
        result = dict()
        result[USER.TIME] = 0
        result[USER.ID] = self.data[USER.ID]
        result[USER.IS_BOT] = self.data[USER.IS_BOT]
        result[USER.FIRST_NAME] = self.data[USER.FIRST_NAME]
        result[USER.USERNAME] = self.data[USER.USERNAME]
        result[USER.LANGUAGE_CODE] = self.data[USER.LANGUAGE_CODE]
        result[USER.ADMIN_RULE] = RIGHT.USER
        result[USER.SOCIAL_NET] = NONE

        return result
