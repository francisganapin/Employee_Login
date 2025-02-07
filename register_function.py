import mysql.connector
from PyQt6.QtCore import QTimer


class RegisterEmployeeClass:
    ''' Employee Registration Logic '''
    
    def __init__(self, ui):
        self.ui = ui  # Store the UI instance

    def register_employee(self):
        # Use `self.ui` to access UI components
        self.employee_id = self.ui.employee_id_input.text()
        self.employee_first_name = self.ui.employee_F_name_input.text()
        self.employee_last_name = self.ui.employee_L_name_input.text()

        # Validate employee ID length
        if len(self.employee_id) != 10:
            self.ui.register_label.setText("Invalid Employee Id. It must be 10 characters.")
            return
        
        try:
            self.employee_rate = float(self.ui.employee_rate_input.text())
        except ValueError:
            self.ui.register_label.setText("Invalid employee rate. Try again.")
            return

        self.employee_position = self.ui.employee_position_input.currentText()

        # Validate required fields
        if not (self.employee_id and self.employee_first_name and self.employee_last_name and self.employee_position):
            self.ui.register_label.setText('Incomplete data. Please fill out all fields.')
            return

        # Check if employee_position is empty
        if not self.employee_position.strip():
            self.ui.register_label.setText('Employee position cannot be empty.')
            return

        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",  # Change this
                database="Employee"  # Change this
            )
            self.cursor = self.connection.cursor()

            # Check if employee already exists
            check_query = "SELECT * FROM employee_data WHERE employee_id = %s"
            self.cursor.execute(check_query, (self.employee_id,))
            result = self.cursor.fetchone()

            if result:
                self.ui.register_label.setText(f'Employee with ID {self.employee_id} already exists.')
            else:
                # Insert new employee
                insert_query = '''
                INSERT INTO employee_data (employee_id, first_name, last_name, employee_rate, employee_position)
                VALUES (%s, %s, %s, %s, %s)'''

                self.cursor.execute(insert_query, (self.employee_id, self.employee_first_name, self.employee_last_name, self.employee_rate, self.employee_position))
                self.connection.commit()

                # Show success message
                self.ui.register_label.setText(f'Employee with ID {self.employee_id} was created.')

                # Clear inputs
                self.ui.employee_id_input.clear()
                self.ui.employee_F_name_input.clear()
                self.ui.employee_L_name_input.clear()
                self.ui.employee_rate_input.clear()
                self.ui.employee_position_input.setCurrentIndex(0)  # Reset dropdown

                # Clear label message after 7 seconds
                QTimer.singleShot(7000, lambda: self.ui.register_label.clear())

            self.cursor.close()
            self.connection.close()

        except mysql.connector.Error as err:
            self.ui.register_label.setText(f"Database error: {err}")
            print(f'Error: {err}')
