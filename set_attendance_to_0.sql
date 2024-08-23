START TRANSACTION;
#SET SQL_SAFE_UPDATES = 0;
#use Employee;

#UPDATE attendance SET attend = 0 WHERE attend = 1;

#COMMIT;
DELETE * FROM employee_data