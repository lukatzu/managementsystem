# This module contains validation functions for employee data.

import re

# Validate JSON data format
# This function checks if the data is a list of employees and validates each employee's data.

def validate_employees_data(employees):
    if not isinstance(employees, list):
        raise ValueError("Data must be a list of employees")

    ids = set()
    for emp in employees:
        if not all(k in emp for k in ["ID", "name", "department", "salary"]):
            raise ValueError("Invalid employee data format")
        if emp['ID'] in ids:
            raise ValueError("Duplicate employee IDs found")
        ids.add(emp['ID'])

# Validate employee name
# This function checks if the name is not empty and contains only letters and spaces.

def validate_name(name):
    if not name or not re.match("^[a-zA-Z ]+$", name):
        raise ValueError("Name cannot contain special characters or numbers")

# Validate department name
# This function checks if the department is not empty and contains only letters and spaces.

def validate_department(dept):
    if not dept or not re.match("^[a-zA-Z ]+$", dept):
        raise ValueError("Department cannot contain special characters or numbers")

# Validate salary
# This function checks if the salary is a valid number and not negative.

def validate_salary(salary_str):
    try:
        salary = int(salary_str)
        if salary < 0:
            raise ValueError("Salary cannot be negative")
        return salary
    except ValueError:
        raise ValueError("Salary must be a valid number")
    
def validate_percent(percent_str):
    try:
        return float(percent_str)
    except ValueError:
        raise ValueError("Adjust Salary (%) must be a valid number")