import mysql.connector as mydb

db_connection = None

try:
    db_connection = mydb.connect(
        user='sample_user',  # ユーザー名
        password='sample_password',  # パスワード
        port='3306',
        host='db_container'  # ホスト名(IPアドレス）
    )

    if db_connection.is_connected:
        print("Connected!")

except Exception as e:
    print(f"Error: {e}")

finally:
    if db_connection is not None and db_connection.is_connected():
        db_connection.close()