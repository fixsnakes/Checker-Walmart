import os, time
from datetime import datetime

import mysql.connector



list_date = str(datetime.now())
date = list_date.split(" ")

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
id = str(33887)
query = f"UPDATE raw_accounts SET status = 4, updated_at = '{date[0]}' WHERE id = '{id}'"
cursor = connection.cursor()
cursor.execute(query)
connection.commit()
print(date[0]+date[1])