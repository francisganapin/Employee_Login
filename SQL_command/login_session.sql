CREATE TABLE IF NOT EXISTS login_sessions(
            id INT AUTO_INCREMENT PRIMARY KEY,
            employee_id VARCHAR(40),
            attend BOOLEAN,
            FOREIGN KEY (employee_id) REFERENCES employee_data(employee_id)
        )