# EmployeeManager class to manage employee data in a JSON file

import json # for JSON file handling
import os # for file existence check
from validators import validate_employees_data # for validating employee data

# This class manages employee data, including loading, saving, adding, removing, and updating employees.

# This is the path to the JSON file where employee data is stored.

FILE_PATH = os.path.join(os.path.dirname(__file__), 'employees.json')
class EmployeeManager:

    # Constructor to initialize the EmployeeManager with a filename.

    def __init__(self):
        self.employee_list = self.load_employees()

    # Load employees from the JSON file.
    # If the file does not exist or is empty, return an empty list.

    def load_employees(self):
        try:
            with open(FILE_PATH, 'r') as file:
                employees = json.load(file)
                validate_employees_data(employees)
                return employees
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        except ValueError:
            return []

    # Save employees to the JSON file.


    def save_employees(self):
        with open(FILE_PATH, 'w') as file:
            json.dump(self.employee_list, file, indent=4)

    # Add a new employee to the list and save to the file.

    def add_employee(self, name, department, salary):
        new_employee = {
            "name": name,
            "ID": self.get_next_employee_id(),
            "department": department,
            "salary": salary
        }
        self.employee_list.append(new_employee)
        self.save_employees()
        return new_employee
    
    # Remove an employee by ID and save to the file.

    def remove_employee(self, emp_id):
        self.employee_list = [emp for emp in self.employee_list if emp['ID'] != emp_id]
        self.save_employees()

    # Update an existing employee's information by ID and save to the file.

    def update_employee(self, emp_id, name, department, salary):
        for emp in self.employee_list:
            if emp['ID'] == emp_id:
                emp['name'] = name
                emp['department'] = department
                emp['salary'] = salary
                break
        self.save_employees()

    # Get all employees.

    def get_employees(self):
        return self.employee_list

    # Get the next available employee ID by finding the maximum ID in the list and adding 1.
    # If the list is empty, return 1.

    def get_next_employee_id(self):
        if self.employee_list:
            return max(emp['ID'] for emp in self.employee_list) + 1
        return 1