import sys
from datetime import datetime

#################################third party import
from PyQt6.QtWidgets import QApplication, QDialog, QLineEdit
from PyQt6 import QtWidgets,uic
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtWidgets import QApplication,QStackedWidget, QWidget
import sys
import mysql.connector
from PyQt6.QtGui import QDoubleValidator #SET ONLY NUMERICAL NUMBER INPUT IN YOUR QLINE EDIT

################# only accept letters and space no number
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
#################

#################################
class MyApp(QtWidgets.QWidget):
    ''' display oru data so that it would work
    '''
    def __init__(self):
        try:
            super().__init__()
            uic.loadUi('main.ui', self)
        
            # Set fixed size to prevent resizing
            self.setFixedSize(self.size())

            self.employee_register_submit_bt.clicked.connect(self.register_employee)


            # Allow only letters and spaces
            self.reg_exp = QRegularExpression("[a-zA-Z ]*")
            self.validator = QRegularExpressionValidator(self.reg_exp)
            self.employee_F_name_input.setValidator(self.validator)
            self.employee_L_name_input.setValidator(self.validator)

            #only accept number
            self.employee_rate_input.setValidator(QDoubleValidator(0.0, 9999.99, 2))
            
            # this will automatically create database for you it was on likne 51
            self.create_database()
            self.create_session()



            ##################### date variables
            self.now = datetime.now()
            self.current_date = self.now.date()
            self.current_time = self.now.time()  

            self.login_bt.clicked.connect(self.login_session)
            self.logout_bt.clicked.connect(self.logout_session)

            #self.create_login_session()


        except FileNotFoundError:
            print(f"UI file {uic.loadUi} not found.")

    def create_database(self):

          #connect to my sql and create database  and check if if database is aready exist if not it would create
            try:
                self.connection = mysql.connector.connect(
                    host="localhost",
                    user='root',
                    password='root'
                )

                self.cursor = self.connection.cursor()
                self.database_name = 'Employee'
                self.cursor.execute(f' CREATE DATABASE IF NOT EXISTS {self.database_name} ')

                self.cursor.close()
                self.connection.close()

                print(f'Database{self.database_name}  was created successfully or already exist.')

            except mysql.connector.Error as err:
                print(f'Error{err}')
                return
            #connect to my sql and create database  and check if if database is aready exist if not it would create


    def create_session(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user='root',
                password='root',
                database='Employee'
            )

            self.cursor = self.connection.cursor()
            self.table = 'login_sessions'  # Ensure the table name is consistent

            # Create the table if it doesn't exist
            # seperat time and date so the system wont accept multiple login 
            # USE time so that table can only input time
            self.query_table = f'''
            CREATE TABLE IF NOT EXISTS {self.table} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            employee_id VARCHAR(40),
            login_date DATE,
            login_time TIME,
            logout_item TIME,
            FOREIGN KEY (employee_id) REFERENCES employee_data(employee_id) 
        )
        '''
            

            self.cursor.execute(self.query_table)
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            print('Successfully referenced to employee_data table')

        except mysql.connector.Error as err:
            print(f'Error: {err}')
            return f'Error: {err}'

    def login_session(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user='root',
                password='root',
                database='Employee'
            )

            self.cursor = self.connection.cursor()
            self.table = 'login_sessions'  # Ensure the table name is consistent

            # Get the employee_id from the input
            self.employee_id = self.login_logout_input.text()

            # Check if the employee_id exists in the employee_data table
            check_query = f"SELECT first_name, last_name FROM employee_data WHERE employee_id = %s"
            self.cursor.execute(check_query, (self.employee_id,))
            self.employee = self.cursor.fetchone()

            if self.employee:
                self.duplicate_check_query = f"SELECT id FROM {self.table} WHERE employee_id = %s AND login_date = %s"
                self.cursor.execute(self.duplicate_check_query,(self.employee_id,self.current_date))
                duplicate_login = self.cursor.fetchone()

                if duplicate_login:
                 
                    print(f"Employee {self.employee[0]} {self.employee[1]} has already log in today.")
                    self.login_logout_label.setText(f"Employee {self.employee[0]} {self.employee[1]} has already log in today.")
                else:
                    self.insert_query = f"INSERT INTO {self.table} (employee_id,login_date,login_time) VALUES (%s,%s,%s)"
                    self.cursor.execute(self.insert_query, (self.employee_id,self.current_date,self.current_time))
                    self.connection.commit()

                    
                    print(f"Employee {self.employee[0]} {self.employee[1]} logged in successfully.")
                    self.login_logout_label.setText(f"Employee {self.employee[0]} {self.employee[1]} logged in successfully.")

            else:
                print(f'Employee id was not found')
                self.login_logout_label.setText(f'Employee id was not found')

        except mysql.connector.Error as err:
            print(f'Error: {err}')
            self.login_logout_label.setText(f'Error: {err}')

        finally:
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()

    def logout_session(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user='root',
                password='root',
                database='Employee'
            )

            self.cursor = self.connection.cursor()
            self.table = 'login_sessions'  # Ensure the table name is consistent

            # Get the employee_id from the input
            self.employee_id = self.login_logout_input.text()

            # Check if the employee_id exists in the employee_data table
            check_query = "SELECT first_name, last_name FROM employee_data WHERE employee_id = %s"
            self.cursor.execute(check_query, (self.employee_id,))
            self.employee = self.cursor.fetchone()

            if self.employee:
                # Check if there is a login session for today for the given employee_id
                session_check_query = f"SELECT logout_item FROM {self.table} WHERE employee_id = %s AND login_date = %s"
                self.cursor.execute(session_check_query, (self.employee_id, self.current_date))
                session = self.cursor.fetchone()

                if session:
                    # Check if logout_time is already set
                    if session[0] is None:
                        # Update the logout time for the session
                        update_query = f"UPDATE {self.table} SET logout_item = %s WHERE employee_id = %s AND login_date = %s"
                        self.cursor.execute(update_query, (self.current_time, self.employee_id, self.current_date))
                        self.connection.commit()
                        print('Logout time updated successfully.')
                    else:
                        self.login_logout_label.setText('Logout time already recorded.')
                        print('Logout time already recorded.')
                else:
                    self.login_logout_label.setText('Logout time already recorded.')
                    print('No login session found for today.')
            else:
                self.login_logout_label.setText('Logout time already recorded.')
                print('Employee ID does not exist.')

        except mysql.connector.Error as err:
            print(f'Error: {err}')
            return f'Error: {err}'

        finally:
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()

    def register_employee(self):
        self.employee_id = self.employee_id_input.text()
        self.employee_first_name = self.employee_F_name_input.text()
        self.employee_last_name = self.employee_L_name_input.text()
        
       
            
        try:
            self.employee_rate = float(self.employee_rate_input.text())
        except ValueError:
            self.register_label.setText("Invalid employee rate.Try again.")
            return

        self.employee_position = self.employee_position_input.currentText()


        # Validate all required fields
        if not (self.employee_id and self.employee_first_name and self.employee_last_name and self.employee_position):
            self.register_label.setText('Incomplete data. Please fill out all fields.')
            return  # Exit the function if any required field is missing

        # Check if employee_position is None or empty
        if self.employee_position is None or not self.employee_position.strip():
            self.register_label.setText('Employee position cannot be None or empty.')
            return  # Exit the function if the position is None or empty

        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user='root',
                password='root',
                database='Employee'
            )

            self.cursor = self.connection.cursor()
            self.table = 'employee_data'

            # Create the table if it doesn't exist
            self.query_table = f'''
            CREATE TABLE IF NOT EXISTS {self.table}(
                id INT AUTO_INCREMENT PRIMARY KEY,
                employee_id VARCHAR(20) UNIQUE,
                first_name VARCHAR(40),
                last_name VARCHAR(40),
                employee_rate FLOAT,
                employee_position VARCHAR(40)
            )'''

            self.cursor.execute(self.query_table)
            self.connection.commit()

            # Check if the employee already exists
            check_query = f"SELECT * FROM {self.table} WHERE employee_id = %s"
            self.cursor.execute(check_query, (self.employee_id,))
            result = self.cursor.fetchone()

            if result:
                print(f'Employee with ID {self.employee_id} already exists.')
                self.register_label.setText(f'Employee with ID {self.employee_id} already exists.')
            else:
                # Insert employee data
                self.employee_query = f'''
                INSERT INTO {self.table} (
                    employee_id, 
                    first_name, 
                    last_name, 
                    employee_rate, 
                    employee_position)
                    VALUES (%s, %s, %s, %s, %s)'''

                self.cursor.execute(self.employee_query, (self.employee_id, self.employee_first_name, self.employee_last_name, self.employee_rate, self.employee_position))
                self.connection.commit()
                self.register_label.setText(f'Employee with ID {self.employee_id}')
                print(f'Employee with ID {self.employee_id} and name {self.employee_first_name} was created')

            self.cursor.close()
            self.connection.close()

        except mysql.connector.Error as err:
            print(f'Error: {err}')
            return
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MyApp()
    main_app.show()
    sys.exit(app.exec())