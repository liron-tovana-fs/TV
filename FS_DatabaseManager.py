import enum
import FS_SQLManager as fssql
import FS_AzureTableManager as fsazuretable


class Provider(enum.Enum):
    MS_SQL = 1
    AZURE_TABLE_STORAGE = 2


class DatabaseManager:
    def __init__(self, provider):
        self.__provider = provider

    def save_answer(self, answer_id, question_id, user_id, result):
        print("Provider is", self.__provider)
        if self.__provider == Provider.MS_SQL:
            fssql.save_answer(answer_id, question_id, user_id, result)
        else:
            fsazuretable.save_answer(answer_id, question_id, user_id, result)

    def get_dataframe(self, query):
        print("Provider is", self.__provider)
        if self.__provider == Provider.MS_SQL:
            return fssql.get_dataframe(query)
        else:
            return fsazuretable.get_dataframe(query)


def execute_query(query):
    return fssql.execute_query(query)
