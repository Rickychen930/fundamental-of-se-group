import tkinter as tk
from tkinter import messagebox
import json

from components.button_component import ButtonComponent
from components.label_component import LabelComponent
from views.base_page import BasePage

# from view_models.login_view_model import LoginViewModel

def load_student_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        return {student['email']: student['password'] for student in data}
    except Exception as e:
        print(f"Error: {e}")
        return {}

students_data = load_student_data('students.data')  
subjects_data = ["Math", "Science", "History", "Art","Chemistry"]

class DashboardPage(BasePage):
    def __init__(self, root):
        super().__init__(root)
        self.root.title("Dashboard Page")
        self.current_user = None  
        self.enrolled_subjects = []
        
        
        self.login_window()

    def main_menu(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()

        LabelComponent(self.root, text="Welcome to Dashboard", font=("Arial", 14)).pack(pady=10)
        
        ButtonComponent(self.root, text="Enroll in Subjects", command=self.enrollment_window).pack(pady=5)
        ButtonComponent(self.root, text="View Enrolled Subjects", command=self.view_enrollments).pack(pady=5)
        ButtonComponent(self.root, text="Logout", command=self.login_window).pack(pady=10)


# step2
    def enrollment_window(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Enroll in Subjects (Max 4)", font=("Arial", 14)).pack(pady=10)
        
        # Check if maximum enrollments more  than 4
        if len(self.enrolled_subjects) >= 4:
            messagebox.showwarning("Warning", "You have already enrolled in 4 subjects.")
            self.main_menu()
            return
        
        self.subject_var = tk.StringVar(self.root)
        self.subject_var.set(subjects_data[0])  
        
        tk.OptionMenu(self.root, self.subject_var, *subjects_data).pack(pady=5)
        tk.Button(self.root, text="Enroll", command=self.enroll_subject).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

# step 3 and 4
    def enroll_subject(self):
        selected_subject = self.subject_var.get()
        
        if selected_subject in self.enrolled_subjects:
            messagebox.showinfo("Info", f"You are already enrolled in {selected_subject}.")
            return
        
        
        if len(self.enrolled_subjects) < 4:
            self.enrolled_subjects.append(selected_subject)
            messagebox.showinfo("Success", f"Enrolled in {selected_subject}.")
        else:
            messagebox.showerror("Error", "You reached the enrollment limit of 4 subjects")
        
        self.main_menu() 

    def view_enrollments(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Enrolled Subjects", font=("Arial", 14)).pack(pady=10)
        
        if self.enrolled_subjects:
            for subject in self.enrolled_subjects:
                tk.Label(self.root, text=subject).pack()
        else:
            tk.Label(self.root, text="No subjects enrolled .").pack()

        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)