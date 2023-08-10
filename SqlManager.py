import mysql.connector
from datetime import datetime

class SQL:
    def __init__(self, device):
        self.device  = device


    def GetAccountData(self):
        config = {
            'user': 'vlaapp',
            'password': 'aOzd1$635',
            'host': '11.0.0.199',
            'port': '3306',
            'database': 'vlaapp'
        }
        connection = mysql.connector.connect(**config)
        query = "SELECT * FROM raw_accounts WHERE status = 0 AND script_id = 1 OR status = 2 AND script_id = 1 ORDER BY RAND() LIMIT 1"
        cursor = connection.cursor()
        cursor.execute(query)
        result_set = cursor.fetchall()
        return result_set

    def UpdateSqlStatus(self,status,id):
        config = {
            'user': 'vlaapp',
            'password': 'aOzd1$635',
            'host': '11.0.0.199',
            'port': '3306',
            'database': 'vlaapp'
        }

        connection = mysql.connector.connect(**config)
        list_date = str(datetime.now())
        date = list_date.split(" ")
        if status == "live":
            query = f"UPDATE raw_accounts SET status = 4, updated_at = '{date[0]}' WHERE id = '{id}'"
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
        elif status == "die":
            query = f"UPDATE raw_accounts SET status = 3, updated_at = '{date[0]}' WHERE id = '{id}'"
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

    def GetAllAccountLive(self):
        config = {
            'user': 'vlaapp',
            'password': 'aOzd1$635',
            'host': '11.0.0.199',
            'port': '3306',
            'database': 'vlaapp'
        }
        connection = mysql.connector.connect(**config)
        query = f"SELECT * FROM raw_accounts WHERE status = 4"
        cursor = connection.cursor()
        cursor.execute(query)
        result_set = cursor.fetchall()
        return result_set

    def GetAccountWithDate(self,from_date,to_date):
        config = {
            'user': 'vlaapp',
            'password': 'aOzd1$635',
            'host': '11.0.0.199',
            'port': '3306',
            'database': 'vlaapp'
        }
        connection = mysql.connector.connect(**config)
        query = f"SELECT * FROM raw_accounts WHERE status = 4 AND updated_at >= '{from_date}' AND updated_at <= '{to_date}'"
        cursor = connection.cursor()
        cursor.execute(query)
        result_set = cursor.fetchall()
        return  result_set






