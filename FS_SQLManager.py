import pyodbc
import pandas as pd
import FS_DateManager

CONNECTION_STRING_TOVANA = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=beaver;' \
                    'DATABASE=T1;User ID=sa;Password=1qaz!QAZ;Trusted_Connection=yes;'
CONNECTION_STRING_CUSTOMER = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=beaver\sql2016;' \
                             'DATABASE=Astea_SGI_NRC_BI_DW;User ID=sa;\Password=1qaz!QAZ;Trusted_Connection=yes'


def save_answer(answer_id, question_id, user_id, result):
    query = "INSERT INTO T1.dbo.FS_answers (answer_id, question_id, created_by, created_at, result)" \
            " VALUES('" + answer_id + "', '" + question_id + "', '" + user_id + "','" + \
            FS_DateManager.get_today().strftime("%Y-%m-%d %H:%M:%S") + "', '" + result + "')"

    execute_query(query, True)

def execute_query(query, is_commit=False):
    sql_conn = pyodbc.connect(CONNECTION_STRING_TOVANA)
    cursor = sql_conn.cursor()
    cursor.execute(query)

    if is_commit is not True:
        return cursor.fetchone()
    else:
        sql_conn.commit()


def get_dataframe(query):
    sql_conn = pyodbc.connect(CONNECTION_STRING_CUSTOMER)

    return pd.read_sql(query, sql_conn)