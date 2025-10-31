
--------------------------------------------------------------------

# UTS Fundamentals of Software Development

### Authors: James Grant - 25932625, Ricky - 25507815

# Project Overview

This project is a **University Student Management System** developed for the *Fundamentals of Software Development* assessment.  
It demonstrates the application of **object-oriented programming (OOP)** principles, and both **CLI (Command-Line Interface)** and **GUI (Graphical User Interface)** have been developed.

The system allows **students** to register, log in, and manage their enrolled subjects, while **administrators** can view, group, partition, and remove student records.  
All student data is saved persistently using file-based storage to simulate a lightweight database.

---

### Key Features

- **Student Management** – Create, view, and manage student profiles and subjects.  
- **Subject Enrolment** – Add or remove subjects (up to a maximum of four per student).  
- **Automated Grading** – Each subject receives a random mark and calculated grade (HD, D, C, P, F).  
- **Data Persistence** – All records are saved in `students.data` using Python’s pickle module.  
- **Admin Tools** – View all students, group by grade, partition by pass/fail, and remove students.  
- **Dual Interface** – Supports both a CLI and a GUI interface for interaction.  
- **Error Handling** – Includes validation and custom exception handling for input and process errors.  
- **Robust Exception Management** – Uses `try` and `except` blocks throughout the program to safely handle file operations, invalid inputs, 
and unexpected runtime errors, ensuring the system continues running smoothly without crashing.  


### Technologies Used

- **Language:** Python 3  
- **GUI Framework:** Tkinter  
- **Data Storage:** Pickle students.data   
- **OOP Concepts:** Encapsulation, inheritance, polymorphism, and abstraction  

This project implements a **University Application System** using a **MVC design pattern** in Python with a Tkinter GUI front end.

###  Example Workflow

```text
[View] StudentPage._enrol_subject_flow()
        ↓
[Controller] StudentController.enrol_auto()
        ↓
[Model] Student.enrol_subject(title)
        ↓
[Controller] save_current() → writes updated student
        ↓
[Database] write_to_file()
        ↓
[Disk] db/students.data
```

# System requirements

Python: Version 3.10 or higher.<br>
Tkinter.<br>

No external dependencies.<br>

# Installation and setup instructions

None required.

# Configurations

None required.<br>
NOTE: John Smith john.smith@university.com is available in the DB using password Helloworld123

# How to run, test, use the software

The project can be run in two different modes: **Command-Line Interface (CLI)** and **Graphical User Interface (GUI)**.  
Both modes use the same backend logic and shared data file.

From the project root run the following command > python .\main.py
Select either the **CLI** or **GUI** option.  


--------------------------------------------------------------------