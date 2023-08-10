
#SQl connected
config = {
    'user': 'vlaapp',
    'password': 'aOzd1$635',
    'host': '11.0.0.199',
    'port':'3306',
    'database': 'vlaapp'
}

connection = mysql.connector.connect(**config)

print(connection)

cursor = connection.cursor()

query = "SELECT * FROM raw_accounts WHERE status = 0 AND script_id = 1 OR status = 2 AND script_id = 1 ORDER BY RAND() LIMIT 1"

cursor.execute(query)

result_set = cursor.fetchall()

for row in result_set:
    print(row[1] + '|' + row[2])

# Đóng cursor và kết nối
cursor.close()
connection.close()
