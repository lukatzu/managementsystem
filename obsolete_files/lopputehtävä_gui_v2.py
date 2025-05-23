#Employee Management System with GUI

from tkinter import * # tkinter for GUI components
from tkinter import ttk # tkinter for GUI components
from tkinter import messagebox # messagebox for user notifications
import json # JSON file for employee data storage
import re  # expression validation

class EmployeeGUI:
    # Crete columns for the employee data
    COLUMNS = ('ID', 'Name', 'Department', 'Salary')

    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry('600x400')

        # Load employee data from file
        self.employee_list = self.load_employees()

        # Create tabs for adding and viewing employees
        self.tab_control = ttk.Notebook(root)
        self.add_tab = ttk.Frame(self.tab_control)
        self.view_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.add_tab, text='Add Employee')
        self.tab_control.add(self.view_tab, text='View Employees')

        self.create_add_employee_widgets()
        self.create_view_employees_widgets()

        self.tab_control.pack(expand=1, fill='both')

        # Refresh employee list at start
        self.refresh_employee_list()

        # Track the current sort order for each column
        self.sort_orders = {col: False for col in self.COLUMNS}

    def create_add_employee_widgets(self):
        # Create widgets for adding employees
        center_frame = ttk.Frame(self.add_tab)
        center_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.name_entry = self.create_label_entry(center_frame, "Name:", 0)
        self.dept_entry = self.create_label_entry(center_frame, "Department:", 1)
        self.salary_entry = self.create_label_entry(center_frame, "Salary:", 2)

        ttk.Button(center_frame, text="Add Employee", command=self.add_employee).grid(row=3, column=0, columnspan=2, pady=20)

    def create_view_employees_widgets(self):
        # Create widgets for viewing employees
        self.tree = ttk.Treeview(self.view_tab, columns=self.COLUMNS, show='headings')

        # Create headings for the treeview columns
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

    def create_label_entry(self, parent, text, row):
        # Create a label and entry widget
        ttk.Label(parent, text=text).grid(row=row, column=0, padx=5, pady=5, sticky='e')
        entry = ttk.Entry(parent)
        entry.grid(row=row, column=1, padx=5, pady=5)
        return entry

    def sort_treeview(self, col):
        # Sort treeview when header is clicked
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        items.sort(key=lambda x: int(x[0]) if col in ('ID', 'Salary') else x[0].lower(), reverse=self.sort_orders[col])
        for index, (val, item) in enumerate(items):
            self.tree.move(item, '', index)
        # Toggle the sort order for the next click
        self.sort_orders[col] = not self.sort_orders[col]

    def edit_employee(self):
        # Open edit window for selected employee
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an employee to edit")
            return

        # Get selected item and its values
        item = self.tree.item(selected_item[0])
        emp_id = item['values'][0]

        self.open_edit_window(emp_id, item['values'])

    def open_edit_window(self, emp_id, values):
        # Create edit window
        edit_window = Toplevel(self.root)
        edit_window.title("Edit Employee")
        edit_window.geometry('300x250')  # Adjusted height to accommodate new field

        name_entry = self.create_entry_with_label(edit_window, "Name:", values[1], 0)
        dept_entry = self.create_entry_with_label(edit_window, "Department:", values[2], 1)
        salary_entry = self.create_entry_with_label(edit_window, "Salary:", values[3], 2)

        # Add percentage-based salary adjustment field
        percent_entry = self.create_entry_with_label(edit_window, "Adjust Salary (%):", "", 3)

        def save_changes():
            try:
                self.validate_and_save_employee(emp_id, name_entry, dept_entry, salary_entry, percent_entry)
                edit_window.destroy()
                messagebox.showinfo("Success", "Employee updated successfully")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(edit_window, text="Save Changes", command=save_changes).grid(row=4, column=0, columnspan=2, pady=20)

    def create_entry_with_label(self, parent, text, value, row):
        # Create a label and entry widget with initial value
        ttk.Label(parent, text=text).grid(row=row, column=0, padx=5, pady=5)
        entry = ttk.Entry(parent)
        entry.insert(0, value)
        entry.grid(row=row, column=1, padx=5, pady=5)
        return entry

    def validate_and_save_employee(self, emp_id, name_entry, dept_entry, salary_entry, percent_entry):
        # Validate and save employee data
        if not name_entry.get() or not dept_entry.get():
            raise ValueError("Name and Department cannot be empty")

        if not re.match("^[a-zA-Z0-9 ]*$", name_entry.get()):
            raise ValueError("Name cannot contain special characters")
        if not re.match("^[a-zA-Z0-9 ]*$", dept_entry.get()):
            raise ValueError("Department cannot contain special characters")

        try:
            salary = int(salary_entry.get())
            if salary < 0:
                raise ValueError("Salary cannot be negative")
        except ValueError:
            raise ValueError("Salary must be a valid number")

        # Apply percentage-based salary adjustment if provided
        if percent_entry.get():
            try:
                percent = float(percent_entry.get())
                salary += salary * (percent / 100)
                salary = int(salary)  # Ensure salary remains an integer
            except ValueError:
                raise ValueError("Adjust Salary (%) must be a valid number")

        for emp in self.employee_list:
            if emp['ID'] == emp_id:
                emp['name'] = name_entry.get()
                emp['department'] = dept_entry.get()
                emp['salary'] = salary
                break
        self.save_employees()
        self.refresh_employee_list()

    def remove_employee(self):
        # Remove selected employee with confirmation
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an employee to remove")
            return

        item = self.tree.item(selected_item[0])
        emp_id = item['values'][0]

        confirm = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove employee ID {emp_id}?")
        if confirm:
            self.employee_list = [emp for emp in self.employee_list if emp['ID'] != emp_id]
            self.save_employees()
            self.refresh_employee_list()
            if not self.employee_list:
                messagebox.showinfo("Info", "The employee list is now empty.")
            else:
                messagebox.showinfo("Success", f"Employee ID {emp_id} removed successfully")

    def add_employee(self):
        # Add a new employee
        try:
            self.validate_and_add_employee()
            messagebox.showinfo("Success", f"Employee added with ID: {self.get_next_employee_id() - 1}")
            self.clear_entries()
            self.refresh_employee_list()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def validate_and_add_employee(self):
        # Validate and add employee data
        if not self.name_entry.get():
            raise ValueError("Name cannot be empty")
        if not self.dept_entry.get():
            raise ValueError("Department cannot be empty")

        if not re.match("^[a-zA-Z ]*$", self.name_entry.get()):
            raise ValueError("Name cannot contain special characters or numbers")
        if not re.match("^[a-zA-Z ]*$", self.dept_entry.get()):
            raise ValueError("Department cannot contain special characters or numbers")

        try:
            salary = int(self.salary_entry.get())
            if salary < 0:
                raise ValueError("Salary cannot be negative")
        except ValueError:
            raise ValueError("Salary must be a valid number")

        new_employee = {
            "name": self.name_entry.get(),
            "ID": self.get_next_employee_id(),
            "department": self.dept_entry.get(),
            "salary": salary
        }
        self.employee_list.append(new_employee)
        self.save_employees()

    def get_next_employee_id(self):
        # Get the next employee ID
        if self.employee_list:
            return max(employee['ID'] for employee in self.employee_list) + 1
        return 1

    def search_employee(self):
        # Search for employees by name or department
        search_term = self.search_entry.get().lower()
        filtered_list = [emp for emp in self.employee_list if search_term in emp['name'].lower() or search_term in emp['department'].lower()]
        if not filtered_list:
            messagebox.showinfo("Info", "No employees match your search.")
        self.refresh_employee_list(filtered_list)

    def refresh_employee_list(self, employee_list=None):
        # Refresh the employee list in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        if employee_list is None:
            employee_list = self.employee_list
        for emp in employee_list:
            self.tree.insert('', 'end', values=(emp['ID'], emp['name'], emp['department'], emp['salary']))

    def clear_entries(self):
        # Clear the entry fields
        self.name_entry.delete(0, END)
        self.dept_entry.delete(0, END)
        self.salary_entry.delete(0, END)

    def load_employees(self):
        # Load employee data from JSON file
        try:
            with open('employees.json', 'r') as file:
                employees = json.load(file)
                # Validate employee data structure
                for emp in employees:
                    if not all(key in emp for key in ["ID", "name", "department", "salary"]):
                        raise ValueError("Invalid employee data format")
                # Check for duplicate IDs
                ids = [emp['ID'] for emp in employees]
                if len(ids) != len(set(ids)):
                    raise ValueError("Duplicate employee IDs found in the data file")
                return employees
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showwarning("Warning", "Employee data file is missing or corrupted. Starting with an empty list.")
            return []
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return []

    def save_employees(self):
        # Save employee data to JSON file
        with open('employees.json', 'w') as file:
            json.dump(self.employee_list, file, indent=4)

    def on_closing(self):
        # Handle application closing
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()

# Initialize the window
root = Tk()
app = EmployeeGUI(root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.mainloop()