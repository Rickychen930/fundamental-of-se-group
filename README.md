Student: alice@university.com / Password123
Admin: admin@university.com / AdminPass123

UTS Fundamentals of Software Development — MVC + MVVM Architecture

This project implements a University Application System using a hybrid MVC + MVVM architecture in Python with Tkinter GUI and a local file database (students.data).

--------------------------------------------------------------------------------
Goal: Clear Mental Model of the Architecture
--------------------------------------------------------------------------------

This project isn’t a pure MVC (Model–View–Controller); it’s a hybrid MVC + MVVM, because:

- The GUI pages (Views) use ViewModels as logic mediators.
- The Controllers manage business rules and data persistence.
- The Models define your data and enforce system constraints.

--------------------------------------------------------------------------------
The 5 Core Layers
--------------------------------------------------------------------------------

USER → VIEW (GUI Page)
         ↓
     CONTROLLER
         ↓
       MODEL
         ↓
     DATABASE (students.data)

Each layer has a clear responsibility and direction of communication.

--------------------------------------------------------------------------------
1️⃣ View = GUI Pages (Tkinter)
--------------------------------------------------------------------------------

Files:
views/login_page.py
views/register_page.py
views/enrolment_page.py
views/admin_page.py

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
2️⃣ Controllers = Business Logic + Data Coordination
--------------------------------------------------------------------------------

Files:
controllers/student_controller.py
controllers/admin_controller.py
controllers/university_controller.py
controllers/subject_controller.py

Purpose:
Controllers are the brains of the system. They connect the ViewModels to the Models and the Database.

Responsibilities:
- Handle CRUD operations (Create, Read, Update, Delete)
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
- UniversityController – Entry point for the application, switches between student/admin modules.
- StudentController – Handles login, registration, enrolment, subject removal, and password changes.
- AdminController – Lists, groups, partitions, removes, or clears student data.
- SubjectController – Manages subject-specific operations such as adding or removing subjects.

--------------------------------------------------------------------------------
3️⃣ ViewModel = Page Logic Layer
--------------------------------------------------------------------------------

Files:
view_models/login_view_model.py
view_models/register_view_model.py

Purpose:
Handles all page-specific logic such as validating user input, interpreting controller responses, and providing information back to the GUI.

Responsibilities:
- Validate user credentials and formats.
- Call the appropriate controller methods.
- Return success or error messages to the View.
- Contain no GUI code (pure logic).

Example:

def login(self):
    ok, msg = self.validate_credentials()
    if not ok:
        return False, msg
    success, result = self.student_controller.login(self.username, self.password)
    if success:
        return True, {"message": "Welcome!", "role": "student"}
    return False, {"message": "Invalid credentials", "role": None}

The ViewModel acts as a bridge between the View (Tkinter GUI) and the Controller (application logic).  
It ensures the GUI layer never interacts directly with data logic.

--------------------------------------------------------------------------------
4️⃣ Models = Core Data and Business Rules
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
5️⃣ Database = Data Persistence Layer
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
