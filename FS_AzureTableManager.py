from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.tablebatch import TableBatch
from azure.cosmosdb.table.models import Entity
import pandas as pd

ACCOUNT_NAME = "myqueueitems01"
ACCOUNT_KEY = "7CKfUUGvryAaD8d8TrqthPoRHemTzXXMCHfckbI/ohZyKey63V2d01DxL6E/lUKkCH+OC6cqxWuyCWZ32THXsA=="

table_service = TableService(account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)


def save_answer(answer_id, question_id, user_id, result):
    answer = Entity()
    answer.PartitionKey = answer_id
    answer.RowKey = question_id
    answer.result = result
    answer.created_by = user_id

    table_service.insert_entity('fsanswers', answer)


def get_answer(answer_id):
    return ""
