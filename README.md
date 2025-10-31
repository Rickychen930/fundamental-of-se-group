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

### Example Workflow

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

# Libraries

inspect: Provides tools for introspecting live Python objects like functions, classes, and modules.

tkinter: A built-in GUI library for creating desktop applications with windows, buttons, and other widgets.

typing: Enables type hints and static type checking to improve code clarity and reliability.

**future**: Allows you to import features from future Python versions for forward compatibility.

os: Offers functions to interact with the operating system, including file paths and environment variables.

platform: Retrieves information about the system’s hardware, OS, and Python version.

dataclasses: Simplifies class creation for storing structured data by auto-generating common methods.

random: Generates pseudo-random numbers for simulations, games, and randomized algorithms.

re: Supports regular expressions for advanced string matching and manipulation.

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

# Classes

## View

view is the folder that include all of interface for user

### GUI

app.py = root file
base_page.py = parent file for GUI
enrolment_page.py = it will show the dashboard including enroll sobject button and show the subjects are enrolled
login_page.py = login
splash_page = this is to load the data

### CLI

admin_page.py = this class is including the CLI view or andmin
app.py = root file
base_page.py = this is for the main menu
student_page.py = this class for student menu

# controller

## AdminController

Handles admin-side business logic for managing student data.

### Methods:

**init**(db: Database): Initializes with a database instance.

\_load_students() -> list[Student]: Loads all student records from the database.

\_write_students(students: list[Student]) -> None: Saves the updated student list to the database.

list_students() -> list[dict]: Returns a list of student data in dictionary format for display.

group_by_grade() -> dict[str, list[Student]]: Groups students by their grade level.

partition_pass_fail() -> dict[str, list[Student]]: Separates students into "pass" and "fail" categories.

remove_student_by_id(student_id: str) -> bool: Deletes a student by ID and returns success status.

clear_all_students() -> bool: Removes all student records from the database.

## StudentController

Manages student-specific operations like authentication and profile updates.

### Methods:

**init**(db: Database): Initializes with a database instance.

\_load_students() -> List[Student]: Loads student records.

\_write_students(students: List[Student]) -> None: Saves student records.

\_save_current_profile() -> None: Persists the currently logged-in student's profile.

find_by_email(email: str) -> Optional[Student]: Finds a student by email.

email_exists(email: str) -> bool: Checks if an email is already registered.

login(email: str, password: str) -> tuple[bool, Optional[str]]: Authenticates a student and returns status and message.

register(name: str, email: str, password: str) -> tuple[bool, str]: Registers a new student and returns status and message.

change_password(new_password: str, confirm: str) -> tuple[bool, str]: Updates the password if confirmation matches.

## SubjectController

Handles subject enrollment and performance tracking for the current student.

### Methods:

**init**(db: Database, current_student: Optional[Student] = None): Initializes with a database and optionally a student.

set_current_student(student: Student) -> None: Sets the active student context.

can_enrol_more() -> bool: Checks if the student can enroll in more subjects.

enrol_auto() -> Tuple[bool, str, Optional[Subject]]: Automatically enrolls the student in a subject and returns status, message, and subject.

list_subjects() -> List[Subject]: Lists all subjects the student is enrolled in.

remove_by_id(subject_id: str) -> Tuple[bool, str]: Removes a subject by ID and returns status and message.

average() -> Optional[float]: Calculates the student's average score across subjects.

\_persist_current_student() -> None: Saves the current student's subject data.

# model

## User Model

Base class for all users, providing shared identity and validation logic.

### Methods:

validate_email(email: str) -> bool: Checks if the email ends with @university.com using regex.

validate_password(password: str) -> bool: Validates password format (uppercase start, ≥5 letters, ≥3 digits).

verify_password(password: str) -> bool: Compares input password with the stored one for authentication.

gen_student_id() -> str: Generates a random 6-digit student ID as a zero-padded string.

## Admin Model

Extends User with static utilities for managing and analyzing student data.

### Methods:

create(name: str, email: str, password: str) -> Admin: Creates an admin instance with validated credentials.

list_students(students: List[Student]) -> List[dict]: Returns a summary list of students with ID, name, email, subject count, average, and grade.

partition_pass_fail(students: List[Student]) -> Dict[str, List[Student]]: Splits students into "PASS" and "FAIL" groups based on average mark.

remove_student_by_id(students: List[Student], student_id: str) -> Tuple[List[Student], bool]: Removes a student by ID and returns the updated list and success flag.

clear_all_students(students: List[Student]) -> List[Student]: Clears all student records by returning an empty list.

group_by_grade(students: List[Student]) -> Dict[str, List[Student]]: Groups students by their overall grade (HD, D, C, P, F).

overall_grade_for(student: Student) -> Optional[str] : Computes the student's overall grade from their average mark.

## Student Model

Extends User to represent a student with subject enrolment, performance tracking, and password management.

### Methods:

create(name, email, password) -> Student: Creates a new student after validating email and password format.

enrol_subject(title) -> Subject: Enrols the student in a new subject with a random ID and mark.

remove_subject(subject_id) -> bool: Removes a subject by ID from the student’s enrolment list.

change_password(new_password) -> None: Updates the student’s password after validating its format.

average_mark() -> Optional[float]: Calculates the average mark across all enrolled subjects.

has_passed() -> bool: Returns True if the student’s average mark is ≥ 50.

to_dict() -> dict: Serializes the student object into a dictionary for storage.

from_dict(data) -> Student: Reconstructs a student object from a dictionary.

students_from_dicts(data) -> list[Student]: Converts a list of student dictionaries into student objects.

students_to_dicts(students) -> list[dict]: Converts a list of student objects into dictionaries.

## Subject Model

Defines a subject enrolment with unique ID, title, numeric mark, and grade, including grading logic and serialization.

### Methods & Functions:

gen_subject_id() -> str: Generates a random 3-digit subject ID as a zero-padded string.

grade_from_mark(mark: int) -> str: Converts a numeric mark (0–100) into a grade letter ("HD", "D", "C", "P", "F").

to_dict() -> dict: Serializes the subject object into a dictionary for storage or transmission.

from_dict(data: dict) -> Subject: Reconstructs a subject object from a dictionary.

### Constants:

GRADE_ORDER: Defines grade hierarchy for sorting and grouping — ["HD", "D", "C", "P", "F"].

MAX_SUBJECTS: Maximum number of subjects a student can enrol in — 4.

---
