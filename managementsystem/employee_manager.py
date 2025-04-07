# EmployeeManager class to manage employee data in a JSON file

import json

# This class manages employee data, including loading, saving, adding, removing, and updating employees.

class EmployeeManager:

    # Constructor to initialize the EmployeeManager with a filename.

    def __init__(self, filename='employees.json'):
        self.filename = filename
        self.employee_list = self.load_employees()

    # Load employees from the JSON file.
    # If the file does not exist or is empty, return an empty list.

    def load_employees(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    # Save employees to the JSON file.


    def save_employees(self):
        with open(self.filename, 'w') as file:
            json.dump(self.employee_list, file, indent=4)

    # Add a new employee to the list and save to the file.

    def add_employee(self, employee):
        self.employee_list.append(employee)
        self.save_employees()

    # Remove an employee by ID and save to the file.

    def remove_employee(self, emp_id):
        self.employee_list = [emp for emp in self.employee_list if emp['ID'] != emp_id]
        self.save_employees()

    # Update an existing employee's information by ID and save to the file.

    def update_employee(self, emp_id, updated_info):
        for emp in self.employee_list:
            if emp['ID'] == emp_id:
                emp.update(updated_info)
                break
        self.save_employees()

    # Get all employees.

    def get_employees(self):
        return self.employee_list

    # Get the next available employee ID by finding the maximum ID in the list and adding 1.
    # If the list is empty, return 1.

    def get_next_employee_id(self):
        return max((emp["ID"] for emp in self.employee_list), default=0) + 1