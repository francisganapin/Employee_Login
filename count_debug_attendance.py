import sys
import mysql.connector

def check_attendance():
    try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user='root',
                    password='root',
                    database='Employee'
                )

                cursor = connection.cursor()
                stable_2 = 'attendance'
                query = f'''SELECT COUNT(attend)  FROM {stable_2} WHERE attend = TRUE; '''
                cursor.execute(query)
                rows = cursor.fetchall()

                for data in rows:
                    print(data)
                
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

