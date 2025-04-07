# GUI (Graphical User Interface) for Employee Management System

from tkinter import * # Import all tkinter classes and functions
from tkinter import ttk, messagebox # Import ttk for themed widgets and messagebox for pop-up messages
from employee_manager import EmployeeManager # Import EmployeeManager class for managing employee data
from validators import validate_name, validate_department, validate_salary # Import validation functions for employee data

# EmployeeGUI class to create the graphical user interface for the Employee Management System
# This class handles the layout, widgets, and interactions for adding, viewing, editing, and removing employees.

class EmployeeGUI:

    # Define the columns for the treeview that displays employee data
    # This tuple contains the column names for the employee treeview.

    COLUMNS = ('ID', 'Name', 'Department', 'Salary')

    # Constructor to initialize the EmployeeGUI with a root window
    # This method sets up the main window, tabs, and widgets for adding and viewing employees.    

    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry('600x400')

        self.manager = EmployeeManager()
        self.tab_control = ttk.Notebook(root)
        self.add_tab = ttk.Frame(self.tab_control)
        self.view_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.add_tab, text='Add Employee')
        self.tab_control.add(self.view_tab, text='View Employees')

        self.create_add_employee_widgets()
        self.create_view_employees_widgets()

        self.tab_control.pack(expand=1, fill='both')
        self.refresh_employee_list()
        self.sort_orders = {col: False for col in self.COLUMNS}

    # Create widgets for adding an employee
    # This method creates labels, entry fields, and buttons for adding an employee.

    def create_add_employee_widgets(self):
        center_frame = ttk.Frame(self.add_tab)
        center_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.name_entry = self.create_label_entry(center_frame, "Name:", 0)
        self.dept_entry = self.create_label_entry(center_frame, "Department:", 1)
        self.salary_entry = self.create_label_entry(center_frame, "Salary:", 2)

        ttk.Button(center_frame, text="Add Employee", command=self.add_employee).grid(row=3, column=0, columnspan=2, pady=20)

    # Create widgets for viewing employees
    # This method creates a treeview for displaying employee data, along with buttons for editing and removing employees.

    def create_view_employees_widgets(self):
        self.tree = ttk.Treeview(self.view_tab, columns=self.COLUMNS, show='headings')

        for col in self.COLUMNS:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            self.tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(self.view_tab, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        edit_button = ttk.Button(self.view_tab, text="Edit Selected", command=self.edit_employee)
        remove_button = ttk.Button(self.view_tab, text="Remove Selected", command=self.remove_employee)

        search_frame = ttk.Frame(self.view_tab)
        search_frame.pack(pady=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=LEFT, padx=5)
        search_button = ttk.Button(search_frame, text="Search", command=self.search_employee)
        search_button.pack(side=LEFT)

        self.tree.pack(side=LEFT, fill=BOTH, expand=1, padx=10, pady=10)
        scrollbar.pack(side=RIGHT, fill=Y)
        edit_button.pack(pady=5)
        remove_button.pack(pady=5)
        ttk.Button(self.view_tab, text="Refresh List", command=self.refresh_employee_list).pack(pady=5)

    # Create a label and entry field for adding an employee
    # This method creates a label and an entry field for the specified text and row.

    def create_label_entry(self, parent, text, row):
        ttk.Label(parent, text=text).grid(row=row, column=0, padx=5, pady=5, sticky='e')
        entry = ttk.Entry(parent)
        entry.grid(row=row, column=1, padx=5, pady=5)
        return entry

    # Sort the treeview based on the selected column
    # This method sorts the treeview items based on the selected column and toggles the sort order.

    def sort_treeview(self, col):
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        items.sort(key=lambda x: int(x[0]) if col in ('ID', 'Salary') else x[0].lower(), reverse=self.sort_orders[col])
        for index, (val, item) in enumerate(items):
            self.tree.move(item, '', index)
        self.sort_orders[col] = not self.sort_orders[col]

    # Edit an employee's information
    # This method opens a new window to edit the selected employee's information.

    def edit_employee(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an employee to edit")
            return

        item = self.tree.item(selected_item[0])
        emp_id = item['values'][0]
        self.open_edit_window(emp_id, item['values'])

    # Open a new window to edit employee information
    # This method creates a new window with entry fields for editing the employee's information.

    def open_edit_window(self, emp_id, values):
        edit_window = Toplevel(self.root)
        edit_window.title("Edit Employee")
        edit_window.geometry('300x250')

        name_entry = self.create_entry_with_label(edit_window, "Name:", values[1], 0)
        dept_entry = self.create_entry_with_label(edit_window, "Department:", values[2], 1)
        salary_entry = self.create_entry_with_label(edit_window, "Salary:", values[3], 2)
        percent_entry = self.create_entry_with_label(edit_window, "Adjust Salary (%):", "", 3)

        def save_changes():
            try:
                name = name_entry.get()
                dept = dept_entry.get()
                salary = validate_salary(salary_entry.get())

                if percent_entry.get():
                    percent = float(percent_entry.get())
                    salary += int(salary * (percent / 100))

                validate_name(name)
                validate_department(dept)

                self.manager.update_employee(emp_id, {
                    'name': name,
                    'department': dept,
                    'salary': salary
                })
                edit_window.destroy()
                self.refresh_employee_list()
                messagebox.showinfo("Success", "Employee updated successfully")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(edit_window, text="Save Changes", command=save_changes).grid(row=4, column=0, columnspan=2, pady=20)

    # Create an entry field with a label for editing employee information
    # This method creates a label and an entry field for the specified text and row.

    def create_entry_with_label(self, parent, text, value, row):
        ttk.Label(parent, text=text).grid(row=row, column=0, padx=5, pady=5)
        entry = ttk.Entry(parent)
        entry.insert(0, value)
        entry.grid(row=row, column=1, padx=5, pady=5)
        return entry

    # Remove an employee from the list
    # This method removes the selected employee from the list and updates the treeview.

    def remove_employee(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an employee to remove")
            return

        item = self.tree.item(selected_item[0])
        emp_id = item['values'][0]

        confirm = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove employee ID {emp_id}?")
        if confirm:
            self.manager.remove_employee(emp_id)
            self.refresh_employee_list()
            messagebox.showinfo("Success", f"Employee ID {emp_id} removed successfully")

    # Add a new employee to the list
    # This method validates the input data and adds a new employee to the list.

    def add_employee(self):
        try:
            name = self.name_entry.get()
            dept = self.dept_entry.get()
            salary = validate_salary(self.salary_entry.get())
            validate_name(name)
            validate_department(dept)

            new_employee = {
                "name": name,
                "ID": self.manager.get_next_employee_id(),
                "department": dept,
                "salary": salary
            }
            self.manager.add_employee(new_employee)
            messagebox.showinfo("Success", f"Employee added with ID: {new_employee['ID']}")
            self.clear_entries()
            self.refresh_employee_list()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # Search for employees based on name or department
    # This method filters the employee list based on the search term and updates the treeview.

    def search_employee(self):
        search_term = self.search_entry.get().lower()
        filtered = [emp for emp in self.manager.get_employees() if search_term in emp['name'].lower() or search_term in emp['department'].lower()]
        if not filtered:
            messagebox.showinfo("Info", "No employees match your search.")
        self.refresh_employee_list(filtered)

    # Refresh the employee list in the treeview
    # This method clears the treeview and repopulates it with the current employee list.

    def refresh_employee_list(self, employee_list=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if employee_list is None:
            employee_list = self.manager.get_employees()
        for emp in employee_list:
            self.tree.insert('', 'end', values=(emp['ID'], emp['name'], emp['department'], emp['salary']))

    # Clear the entry fields after adding an employee
    # This method clears the entry fields for name, department, and salary.

    def clear_entries(self):
        self.name_entry.delete(0, END)
        self.dept_entry.delete(0, END)
        self.salary_entry.delete(0, END)

    # Close the application with a confirmation dialog
    # This method prompts the user to confirm before closing the application.

    def on_closing(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()