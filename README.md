UTS Fundamentals of Software Development — MVC + MVVM Architecture


Please include:

source code
README
project overview
system requirements
installation and setup instructions
configurations
how to run, test, use the software
Please do not include:

automatically generated build, cache, logs (stuffs generated from running the code)

things that are specific to your local environment (e.g., IDE settings)

dependencies, e.g., node modules



This project implements a University Application System using a hybrid MVC + MVVM architecture in Python with Tkinter GUI and a local file database (students.data).

--------------------------------------------------------------------------------
Goal: Clear Mental Model of the Architecture
--------------------------------------------------------------------------------

This project isn’t a pure MVC (Model–View–Controller); it’s a hybrid MVC + MVVM, because:

- The GUI pages (Views) use ViewModels as logic mediators.
- The Controllers manage business rules and data persistence.
- The Models define your data and enforce system constraints.

--------------------------------------------------------------------------------
The Core Layers
--------------------------------------------------------------------------------

+------------------+
|      View        | ← handles user input/output
| (CLI / GUI pages)|
+--------▲---------+
         |
         | calls
         ▼
+------------------+
|    Controller    | ← business logic (what to do)
| (Admin / Student)|
+--------▲---------+
         |
         | loads/saves data
         ▼
+------------------+
|     Database     | ← raw file I/O (pickled data)
+--------▲---------+
         |
         | stores/loads Python objects
         ▼
+------------------+
|      Models      | ← data definitions & rules
| (Student, Admin) |
+------------------+

Example work flow 

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
[Disk] db/students.data (pickled)

--------------------------------------------------------------------------------
View = GUI Pages (Tkinter)
--------------------------------------------------------------------------------

Files:
views/GUI/login_page.py
views/GUI/register_page.py
views/GUI/enrolment_page.py
views/GUI/admin_page.py

Purpose:
To display information and capture user input — buttons, text fields, and labels.

Responsibilities:
- Show forms (e.g., Login, Register)
- Display enrolled subjects
- Handle button clicks
- Pass input data to the ViewModel

Views do not handle business logic or file I/O.

When a user clicks “Login”, the View calls:

self.view_model.login()

--------------------------------------------------------------------------------
Controllers = Business Logic + Data Coordination
--------------------------------------------------------------------------------

Files:
controller/student_controller.py
controller/admin_controller.py
controller/subject_controller.py

Purpose:
Controllers are the brains of the system. They connect the ViewModels to the Models and the Database.

Responsibilities:
- Load and save data through the Database
- Apply business rules (max 4 subjects, pass/fail logic, unique IDs)
- Never directly manipulate the GUI

Example:

def login(self, email, password):
    raw = self.db.read_from_file() or []
    students = students_from_dicts(raw)
    student = find_student_by_email(students, email)
    if student and student.verify_password(password):
        print("[DEBUG] Login success")
        return True, student.role
    print("[DEBUG] Login failed")
    return False, None

Controllers interact only with Models and the Database, making them reusable for both CLI and GUI applications.

Example Controllers:
- StudentController – Handles login, registration, enrolment, subject removal, and password changes.
- AdminController – Lists, groups, partitions, removes, or clears student data.
- SubjectController – Manages subject-specific operations such as adding or removing subjects.


--------------------------------------------------------------------------------
Models = Core Data and Business Rules
--------------------------------------------------------------------------------

Files:
models/user_model.py
models/student_model.py
models/admin_model.py
models/subject_model.py

Purpose:
Defines all application data structures and the rules that govern them, including Users, Students, Admins, and Subjects.

Responsibilities:
- Represent data entities and enforce validation rules.
- Generate IDs, marks, and grades.
- Implement internal operations such as enrol_subject or change_password.
- Contain all business logic (no GUI or database code).

Example:

def enrol_subject(self, title):
    if len(self.subjects) >= 4:
        raise ValueError("Cannot enrol in more than four subjects.")
    mark = random.randint(25, 100)
    grade = grade_from_mark(mark)
    self.subjects.append(Subject(gen_subject_id(), title, mark, grade))
    return True

Model Relationships:
- User → Student / Admin (inheritance)
- Student → Subject (composition: a student has subjects)
- Admin → Student (dependency: admin manages students)

--------------------------------------------------------------------------------
Database = Data Persistence Layer
--------------------------------------------------------------------------------

File:
db/database.py

Purpose:
Manages all data persistence for the project using Python’s pickle module.  
All system data, including students and admins, are stored in a single local file called students.data.

Responsibilities:
- Create the database file if missing.
- Read and write serialized Python objects.
- Clear file contents when required.
- Provide backward-compatible methods such as read_data and read_from_file.

Example:

def write_to_file(self, data_list):
    with open(self.path, "wb") as f:
        pickle.dump(list(data_list or []), f)
    print(f"[DEBUG][DB] Wrote {len(data_list)} records to {self.path}")

The Database is only accessed by Controllers, never directly by Views or ViewModels.

--------------------------------------------------------------------------------
End of Document
--------------------------------------------------------------------------------
