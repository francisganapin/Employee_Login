 CREATE TABLE IF NOT EXISTS attendance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            employee_id VARCHAR(40),
            login_date DATE,
            login_time TIME,
            logout_item TIME,
            FOREIGN KEY (employee_id) REFERENCES employee_data(employee_id) 
        );
     