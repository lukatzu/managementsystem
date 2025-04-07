# This module contains validation functions for employee data.

import re

# Validate employee name

def validate_name(name):
    if not name or not re.match("^[a-zA-Z ]+$", name):
        raise ValueError("Name cannot contain special characters or numbers")

# Validate department name

def validate_department(dept):
    if not dept or not re.match("^[a-zA-Z ]+$", dept):
        raise ValueError("Department cannot contain special characters or numbers")

# Validate salary input

def validate_salary(salary_str):
    try:
        salary = int(salary_str)
        if salary < 0:
            raise ValueError("Salary cannot be negative")
        return salary
    except ValueError:
        raise ValueError("Salary must be a valid number")