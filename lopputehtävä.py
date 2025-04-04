# 2. Employee Management System without the GUI

""" This code is kinda obselete, but I will keep it for reference."""

import json # importing the json module to handle JSON data

def load_employees():
    # load employees from a JSON file
    try:
        with open('employees.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_employees(employee_list):
    # save employees to a JSON file
    with open('employees.json', 'w') as file:
        json.dump(employee_list, file, indent=4)

# Replace the hardcoded employee_list with loading from JSON
employee_list = load_employees()

# defining a function to add an employee

def add_employee():
    next_id = max(employee['ID'] for employee in employee_list) + 1 if employee_list else 1
    
    new_employee = {
        "name": str(input("Enter the name of the employee: ")),
        "ID": next_id,
        "department": str(input("Enter the department of the employee: ")),
        "salary": int(input("Enter the salary of the employee: "))
    }
    employee_list.append(new_employee)
    print(f"Employee added with ID: {next_id}")

# defining a function to remove an employee

def remove_employee(employee_list):
    name = input("Enter the name of the employee: ")
    for employee in employee_list:
        if employee['name'] == name:
            employee_list.remove(employee)
            print(f"Employee {name} has been removed.")
            return
    print(f"Employee {name} not found.")

# defining a function to update employee details

def update_employee(employee_list):
    name = input("Enter the name of the employee: ")
    found = False
    for employee in employee_list:
        if employee['name'] == name:
            choice = int(input("Select what you want to update: \n2. Department\n3. Salary\n"))
            if choice == 1:
                employee['department'] = input("Enter the new department: ")
            elif choice == 2:
                employee['salary'] = int(input("Enter the new salary: "))
            found = True
            break
    if not found:
        print(f"Employee {name} not found.")


def display_employees(employee_list):
    # display all employees or filter by department
    departments = set(employee['department'] for employee in employee_list)
    department = input(f"Enter the department to filter by Departments: {', '.join(departments)} (leave empty to show all): ")
    for employee in employee_list:
        if department == "":
            print(employee)
        elif employee['department'] == department:
            print(f"Name: {employee['name']} ID: {employee['ID']}")

print("Welcome to the Employee Management System")
# main loop for the program
while True:
    print("\n1. Add Employee\n2. Remove Employee\n3. Update Employee\n4. Display Employees\n5. Exit")
    try:
        choice = int(input("Enter your choice: "))
        if choice == 1:
            add_employee()
            save_employees(employee_list)
        elif choice == 2:
            remove_employee(employee_list)
            save_employees(employee_list)
        elif choice == 3:
            update_employee(employee_list)
            save_employees(employee_list)
        elif choice == 4:
            display_employees(employee_list)
        elif choice == 5:
            save_employees(employee_list)
            break
        else:
            print("Invalid choice. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")

