import mysql.connector

def check_attendance():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user='root',
            password='root',
            database='employee'
        )
        
        cursor = connection.cursor()
        while True:
            employee_id = input('Enter Employee id: ')
            cursor.execute(f"SELECT * FROM employee_data WHERE employee_id = '{employee_id}';")
            result =cursor.fetchone()

            if result:
                break
            else:
                print(f"id you input '{employee_id}' was not exist try again")

        while True:
            try:
                salary = int(input('Put valid Salary: '))
            except ValueError:
                print('invalid Input.Please try again')
            else:
                break
       

        cursor = connection.cursor()
        # Update the employee rate for the specified employee ID
        query = f'''UPDATE employee_data SET employee_rate = {salary} WHERE employee_id = '{employee_id}';'''
        cursor.execute(query)
        
        # Commit the transaction to save changes
        connection.commit()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Execute the function
check_attendance()
