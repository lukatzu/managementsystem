# Author: Luka Niemelä
# Employee Management System

from tkinter import Tk
from gui import EmployeeGUI

# This is the main entry point for the Employee Management System.
# It initializes the GUI and sets up the main application window.

if __name__ == "__main__":
    root = Tk()
    app = EmployeeGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()