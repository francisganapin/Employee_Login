import sys
from datetime import datetime

#################################third party import
from PyQt6.QtWidgets import QApplication
from PyQt6 import QtWidgets,uic
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication,QStackedWidget, QWidget
import sys
import mysql.connector
from PyQt6.QtGui import QDoubleValidator #SET ONLY NUMERICAL NUMBER INPUT IN YOUR QLINE EDIT
from PyQt6.QtCore import QTimer
################# only accept letters and space no number
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
#################
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget
from PyQt6.QtGui import QStandardItemModel, QStandardItem

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

            # Create the table view and set up the model
            self.model_1 = QStandardItemModel()
            self.model_1.setHorizontalHeaderLabels(["Id", "Employee id", "First Name", "Last Name", "Rate", "Position"])
            self.tableView.setModel(self.model_1)


            
            # Create the table view and set up the model
            self.model_2 = QStandardItemModel()
            self.model_2.setHorizontalHeaderLabels(["Id", "Employee id", "Attend"])
            self.tableView_2.setModel(self.model_2)

            self.model_3 = QStandardItemModel()
            self.model_3.setHorizontalHeaderLabels(['Id','Employee Id','Date','Login','Logout'])
            self.tableView_3.setModel(self.model_3)

            self.employee_register_submit_bt.clicked.connect(self.register_employee)


            # Allow only letters and spaces
            self.reg_exp = QRegularExpression("[a-zA-Z ]*")
            self.validator = QRegularExpressionValidator(self.reg_exp)
            self.employee_F_name_input.setValidator(self.validator)
            self.employee_L_name_input.setValidator(self.validator)

            #only accept number
            self.employee_rate_input.setValidator(QDoubleValidator(0.0, 9999.99, 2))
            self.employee_rate_input_salary.setValidator(QDoubleValidator(0.0, 9999.99, 2))
            
            # this will automatically create database for you it was on likne 51
            self.create_database()
            self.create_session()
            self.show_data_base()
            self.show_attendance_attendance()
            self.show_login_session()



            ##################### date variables
            self.now = datetime.now()
            self.current_date = self.now.date()
            self.current_time = self.now.time()  

            self.login_bt.clicked.connect(self.login_session)
            self.logout_bt.clicked.connect(self.logout_session)

            #self.create_login_session()

            self.close_register_bt.clicked.connect(self.homepage_page)
            self.close_bt_2.clicked.connect(self.homepage_page)
            self.add_employee.clicked.connect(self.register_page_bt)
            self.login_logout_bt.clicked.connect(self.login_logout_page)
            self.debug_page_bt.clicked.connect(self.debug_page)
            self.clear_attendance_bt.clicked.connect(self.clear_attendance)
            self.close_bt_5.clicked.connect(self.homepage_page)
            self.check_attenance_bt.clicked.connect(self.check_attendance)
            self.update_salary_bt.clicked.connect(self.updateSalary)
            self.close_bt_salary.clicked.connect(self.homepage_page)
            self.salary_bt_page.clicked.connect(self.salary_page)
            self.submit_delete.clicked.connect(self.delete_employee)
            self.refresh_data_bt.clicked.connect(self.show_data_base)
            self.search_session_bt.clicked.connect(self.search_login_session)
            self.submit_attendance_bt.clicked.connect(self.search_attend_session)
            self.close_bt_6.clicked.connect(self.homepage_page)
            self.login_record_bt.clicked.connect(self.record_page_gui)
            # Pages
            self.stackedWidget = self.findChild(QStackedWidget, 'stackedWidget')
            self.employee_login_logout_page = self.findChild(QWidget, 'employee_login_logout') # Get started page
            self.register_page_1 = self.findChild(QWidget, 'reg_page')
            self.homepage = self.findChild(QWidget, 'homepage')
            self.debug_page_1 = self.findChild(QWidget, 'debug_page_1')
            self.login_record_page = self.findChild(QWidget, 'record_page')
            self.update_salary_page = self.findChild(QWidget,'update_salary_page')

        # Fetch and display data
            self.show_data_base()


            self.config_server = {
                'host':"localhost",
                'user':'root',
                'password':'root',
                'database':'Employee'
                }
            

        except FileNotFoundError:
            print(f"UI file {uic.loadUi} not found.")
    

  

    def debug_page(self):
        self.stackedWidget.setCurrentWidget(self.debug_page_1)

    def login_logout_page(self):
        self.stackedWidget.setCurrentWidget(self.employee_login_logout_page)

    def homepage_page(self):
        self.stackedWidget.setCurrentWidget(self.homepage)

    def register_page_bt(self):
         self.stackedWidget.setCurrentWidget(self.register_page_1)

         # it goes to salary page update salary page
    def salary_page(self):
        self.stackedWidget.setCurrentWidget(self.update_salary_page)
    
    def record_page_gui(self):
        self.stackedWidget.setCurrentWidget(self.login_record_page)


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
            self.connection = mysql.connector.connect()

            self.cursor = self.connection.cursor()
            self.table = 'login_sessions'  # Ensure the table name is consistent
            self.table_2 = 'attendance'

            # Create the table if it doesn't exist
            self.query_table = f'''
            CREATE TABLE IF NOT EXISTS {self.table} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                employee_id VARCHAR(40),
                login_date DATE,
                login_time TIME,
                logout_item TIME
            )
            '''
            
            self.query_table_2 = f'''
            CREATE TABLE IF NOT EXISTS {self.table_2}(
                id INT AUTO_INCREMENT PRIMARY KEY,
                employee_id VARCHAR(40),
                attend BOOLEAN
            )
            '''
                
            # Create the employee_data table if it doesn't exist
            self.query_table_3 = f'''
            CREATE TABLE IF NOT EXISTS employee_data(
                id INT AUTO_INCREMENT PRIMARY KEY,
                employee_id VARCHAR(20) UNIQUE,
                first_name VARCHAR(40),
                last_name VARCHAR(40),
                employee_rate FLOAT,
                employee_position VARCHAR(40)
            )
            '''

            # Execute the table creation queries
            self.cursor.execute(self.query_table)
            self.cursor.execute(self.query_table_2)
            self.cursor.execute(self.query_table_3)
            
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            print('Successfully referenced to employee_data table')

        except mysql.connector.Error as err:
            print(f'Error: {err}')
            return f'Error: {err}'


    def login_session(self):
        try:
            self.connection = mysql.connector.connect(**self.config_server)

            self.cursor = self.connection.cursor()
            self.table = 'login_sessions'  # Ensure the table name is consistent
            self.table_2 = 'attendance'

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

                    self.check_attendance_query = f"SELECT id FROM {self.table_2} WHERE employee_id = %s"
                    self.cursor.execute(self.check_attendance_query, (self.employee_id,))
                    attendance_record = self.cursor.fetchone()

                    if attendance_record:
                        self.update_attendance_query = f"UPDATE {self.table_2} SET attend = TRUE WHERE employee_id = %s"
                        self.cursor.execute(self.update_attendance_query, (self.employee_id,))
                    else:
                        self.insert_attendance_query = f"INSERT INTO {self.table_2} (employee_id, attend) VALUES (%s, TRUE)"
                        self.cursor.execute(self.insert_attendance_query, (self.employee_id,))

                self.connection.commit()

            else:
                print(f'Employee id was not found')
                self.login_logout_label.setText(f'Employee id was not found')

        except mysql.connector.Error as err:
            print(f'Error: {err}')
            self.login_logout_label.setText(f'Error: {err}')

    def logout_session(self):
        try:
            self.connection = mysql.connector.connect(**self.config_server)

            self.cursor = self.connection.cursor()
            self.table = 'login_sessions'
            self.table_2 = 'attendance'

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

                        # Update or insert attendance record
                        self.check_attendance_query = f"SELECT id FROM {self.table_2} WHERE employee_id = %s"
                        self.cursor.execute(self.check_attendance_query, (self.employee_id,))
                        attendance_record = self.cursor.fetchone()

                        if attendance_record:
                            self.update_attendance_query = f"UPDATE {self.table_2} SET attend = FALSE WHERE employee_id = %s"
                            self.cursor.execute(self.update_attendance_query, (self.employee_id,))
                        else:
                            self.insert_attendance_query = f"INSERT INTO {self.table_2} (employee_id, attend) VALUES (%s, FALSE)"
                            self.cursor.execute(self.insert_attendance_query, (self.employee_id,))

                        self.connection.commit()

                    else:
                        self.login_logout_label.setText('Logout time already recorded.')
                        print('Logout time already recorded.')
                else:
                    self.login_logout_label.setText('No login session found for today.')
                    print('No login session found for today.')
            else:
                self.login_logout_label.setText('Employee ID does not exist.')
                print('Employee ID does not exist.')

        except mysql.connector.Error as err:
            print(f'Error: {err}')
            self.login_logout_label.setText(f'Error: {err}')

        finally:
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()

    def register_employee(self):
        self.employee_id = self.employee_id_input.text()
        self.employee_first_name = self.employee_F_name_input.text()
        self.employee_last_name = self.employee_L_name_input.text()




        if len(self.employee_id) != 10:
                self.register_label.setText("Invalid Employee Id  it must 10 character")
                return
            
        
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
            self.connection = mysql.connector.connect(**self.config_server)
            self.cursor = self.connection.cursor()
            # Check if the employee already exists
            check_query = f"SELECT * FROM  employee_data WHERE employee_id = %s"
            self.cursor.execute(check_query, (self.employee_id,))
            result = self.cursor.fetchone()

            if result:
                print(f'Employee with ID {self.employee_id} already exists.')
                self.register_label.setText(f'Employee with ID {self.employee_id} already exists.')
            else:
                # Insert employee data
                self.employee_query = f'''
                INSERT INTO employee_data (
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

                self.register_label.setText(f'Employee with ID {self.employee_id} was created')

                self.employee_position_input.clear()
                self.employee_id_input.clear()
                self.employee_F_name_input.clear()
                self.employee_L_name_input.clear()
                QTimer.singleShot(7000, lambda: self.register_label.clear())

            self.cursor.close()
            self.connection.close()

        except mysql.connector.Error as err:
            print(f'Error: {err}')
            return
        

    def check_attendance(self):
        try:
            connection = mysql.connector.connect(**self.config_server)

            cursor = connection.cursor()
            stable_2 = 'attendance'
            query =  f"SELECT COUNT(*) FROM {stable_2} WHERE attend = 1"
            cursor.execute(query)
            
            rows = cursor.fetchall()

            if rows:
                for data in rows:
                    self.str_attendance = str(data[0])
                    self.attendance_label.setText(self.str_attendance)
            else:
                self.attendance_label.setText("No records found.")
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            print('none')

    
    def clear_attendance(self):
        try:
                    connection = mysql.connector.connect(**self.config_server)

                    cursor = connection.cursor()
    
                    query = f'''UPDATE attendance SET attend = 0 WHERE attend = 1'''
                    cursor.execute(query)
                    connection.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

            
        finally:
           print('wow')


        
    def updateSalary(self):
        '''Update salary of employee '''
        self.employee_rate = self.employee_rate_input_salary.text()
        self.employee_id = self.employee_id_input_salary.text()
        
        try:
            connection = mysql.connector.connect(**self.config_server)
            cursor = connection.cursor()
            
            # Check if employee_id exists
            cursor.execute(f"SELECT * FROM employee_data WHERE employee_id = '{self.employee_id}';")
            result = cursor.fetchone()

            if not result:
                self.salary_label_update.setText("Invalid employee ID. Please try again.")
                return  # Exit the function if the employee ID is invalid
            
            # Validate the salary input
            try:
                self.employee_rate = int(self.employee_rate)
            except ValueError:
                self.salary_label_update.setText("Invalid salary input. Please enter a valid number.")
                return  # Exit the function if the salary is invalid
            
            # Update the employee rate in the database
            query = f"UPDATE employee_data SET employee_rate = {self.employee_rate} WHERE employee_id = '{self.employee_id}';"
            cursor.execute(query)
            connection.commit()

            self.salary_label_update.setText("Salary updated successfully.")
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def show_data_base(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user='root',
                password='root',
                database='Employee'
            )
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM employee_data;")
            rows = cursor.fetchall()

            # Clear existing data in the model
            self.model_1.removeRows(0, self.model_1.rowCount())

            for row_data in rows:
                items = [QStandardItem(str(data)) for data in row_data]
                self.model_1.appendRow(items)

            print('Data Fetched Successfully')

        except mysql.connector.Error as e:
            print(f'MySQL error: {e}')

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


    def show_attendance_attendance(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='Employee'
            )
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM attendance')
            rows = cursor.fetchall()

            self.model_2.removeRows(0,self.model_2.rowCount())

            for row_data in rows:
                items =[QStandardItem(str(data)) for data in row_data]
                self.model_2.appendRow(items)

            print('Data Fetched sucessfully')
        except mysql.connector.Error as e:
            print(f'')
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()




    def show_login_session(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='Employee'
            )
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM login_sessions')
            rows = cursor.fetchall()

            self.model_3.removeRows(0,self.model_3.rowCount())

            for row_data in rows:
                items =[QStandardItem(str(data))for data in row_data]
                self.model_3.appendRow(items)
            
        except mysql.connector.Error as e:
            print('g')
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def search_login_session(self):

        self_employee_login_session = self.login_session_input.text()
        connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='Employee'
            )
        self.cursor = connection.cursor()
        self.query= 'SELECT id,employee_id,login_date,login_time,logout_item FROM login_sessions WHERE 1=1'
        self.params = []
        
        if self_employee_login_session:
            self.query += ' AND employee_id LIKE %s'
            self.params.append(f"%{self_employee_login_session}%")

        try: 
            self.cursor.execute(self.query, self.params)
            self.rows = self.cursor.fetchall()
            self.model_3.removeRows(0, self.model_3.rowCount())

            for row_data in self.rows:
                items = [QStandardItem(str(data)) for data in row_data]
                self.model_3.appendRow(items)

            print('Search Results Fetched Successfully')
        except mysql.connector.Error as e:
            print(f'Sqlite error: {e}')
        finally:
            if connection.is_connected():
                self.cursor.close()
                connection.close()

    def delete_employee(self):
        self.employee_id_2 = self.employee_id_input_2.text()

        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='Employee'
            )
            cursor = connection.cursor()
            
            # Use parameterized query to prevent SQL injection
            delete_query = f"DELETE FROM employee_data WHERE employee_id = '{self.employee_id_2}'"
            cursor.execute(delete_query)
            connection.commit()

            if cursor.rowcount == 0:
                self.delete_validator_page.setText('Invalid employee ID. Try again.')
            else:
                self.delete_validator_page.setText('Employee deleted successfully.')

        except mysql.connector.Error as e:
            print(f'MySQL error: {e}')

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


    def search_login_session(self):

        self_employee_login_session = self.login_session_input.text()
        connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='Employee'
            )
        self.cursor = connection.cursor()
        self.query= 'SELECT id,employee_id,login_date,login_time,logout_item FROM login_sessions WHERE 1=1'
        self.params = []
        
        if self_employee_login_session:
            self.query += ' AND employee_id LIKE %s'
            self.params.append(f"%{self_employee_login_session}%")

        try: 
            self.cursor.execute(self.query, self.params)
            self.rows = self.cursor.fetchall()
            self.model_3.removeRows(0, self.model_3.rowCount())

            for row_data in self.rows:
                items = [QStandardItem(str(data)) for data in row_data]
                self.model_3.appendRow(items)

            print('Search Results Fetched Successfully')
        except mysql.connector.Error as e:
            print(f'Sqlite error: {e}')
        finally:
            if connection.is_connected():
                self.cursor.close()
                connection.close()


    def search_attend_session(self):

        self.employee_attendance = self.employee_id_input_3.text()
        connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='Employee'
            )
        self.cursor = connection.cursor()
        self.query= 'SELECT id,employee_id,attend FROM attendance WHERE 1=1'
        self.params = []
        
        if self.employee_attendance:
            self.query += ' AND employee_id LIKE %s'
            self.params.append(f"%{self.employee_attendance}%")

        try: 
            self.cursor.execute(self.query, self.params)
            self.rows = self.cursor.fetchall()
            self.model_2.removeRows(0, self.model_2.rowCount())

            for row_data in self.rows:
                items = [QStandardItem(str(data)) for data in row_data]
                self.model_2.appendRow(items)

            print('Search Results Fetched Successfully')
        except mysql.connector.Error as e:
            print(f'Sqlite error: {e}')
        finally:
            if connection.is_connected():
                self.cursor.close()
                connection.close()

        
if __name__ == "__main__":
    app = QApplication([])
    main_app = MyApp()
    main_app.show()
    app.exec()