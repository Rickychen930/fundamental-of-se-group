# 🧩 Admin Controls — Workflow Overview

The **Admin system** in the CLI follows a clear **MVC flow** for every menu option:

| Key | Action | Purpose |
|-----|---------|----------|
| **c** | Clear Database | Removes all student records |
| **g** | Group by Grade | Groups students by grade (HD–F) |
| **p** | Partition Pass/Fail | Splits students into PASS and FAIL |
| **r** | Remove Student | Deletes a student by ID |
| **s** | Show All Students | Lists all registered students |

Each action flows through **View → Controller → Model → Database**.  
Below is a detailed breakdown for each.

---

## `c` — Clear Students Database

```
Admin presses 'c'
  AdminPage._clear_students_flow()
    └─► AdminController.clear_all_students()
          └─► _write_students([])               # write empty list
                └─► Database.write_to_file([])  # overwrite data file
Back to AdminPage → "Students data cleared"
```

### **Flow Summary**
- **View (AdminPage)**: asks for confirmation, calls controller.
- **Controller (AdminController)**: writes an empty list.
- **Database**: overwrites `db/students.data` with `[]`.
- **Model**: not used here.
- **View**: displays “Students data cleared”.

### **Result**
All student data is erased, but the file still exists (just empty).

---

## 🎓 `g` — Group Students by Grade

```
Admin presses 'g'
  AdminPage.show_grade_grouping()
    └─► AdminController.group_by_grade()
          └─► Admin.group_by_grade(students)
                └─► overall_grade_for(s) → grade_from_mark(...)
Back to AdminPage:
  sort each grade list by average (desc)
  display in order: HD → D → C → P → F
```

### **Flow Summary**
- **Controller** loads students from the database.
- **Model (Admin)** computes each student’s grade:
  - Uses `overall_grade_for()` → `grade_from_mark()`.
  - Returns a dictionary:  
    `{ "HD": [...], "D": [...], "C": [...], "P": [...], "F": [...] }`.
- **View (AdminPage)**:
  - Sorts students within each grade group by average mark (descending).
  - Prints results in grade order (HD → F).

### **Result**
All students are displayed grouped by grade, sorted by their averages.

---

## ✅ `p` — Partition Students into PASS / FAIL

```
Admin presses 'p'
  AdminPage.show_partition()
    └─► AdminController.partition_pass_fail()
          └─► Admin.partition_pass_fail(students)
                └─► Student.average_mark()  # inside loop
Back to AdminPage:
  sort each list by average mark (desc)
  print:
    FAIL --> [...]
    PASS --> [...]
```

### **Flow Summary**
- **Controller** loads all students.
- **Model (Admin)**:
  - Calculates each student’s average using `Student.average_mark()`.
  - Adds to `"PASS"` if avg ≥ 50, else `"FAIL"`.
  - Skips students with no marks.
  - Returns:
    ```python
    {"PASS": [Student(...), ...], "FAIL": [Student(...), ...]}
    ```
- **View**:
  - Sorts each list by average (descending).
  - Prints FAIL first, then PASS.

### **Result**
Students are split into PASS and FAIL groups and displayed neatly.

---

## ❌ `r` — Remove a Student by ID

```
Admin presses 'r'
  AdminPage.remove_student_flow()
    └─► AdminController.remove_student_by_id(sid)
          └─► Admin.remove_student_by_id(students, sid)
                └─► filter out matching ID → (updated_list, removed=True/False)
Back to AdminController:
    if removed → _write_students(updated)
                     └─► Database.write_to_file(updated)
Back to AdminPage:
    print success or "Student does not exist"
```

### **Flow Summary**
- **View** asks for a student ID.
- **Controller**:
  - Loads all students.
  - Calls the **Admin model** to remove by ID.
  - If a match is found, saves the updated list back to the database.
- **Model (Admin)**:
  - Filters the list of students:
    ```python
    filtered = [s for s in students if s.id != sid]
    ```
  - Returns updated list and a removal flag.
- **View** shows either success or error message.

### **Result**
The selected student is permanently removed from the database.

---

## 👩‍🎓 `s` — Show All Students

```
Admin presses 's'
  AdminPage.show_all()
    └─► AdminController.list_students()
          └─► Admin.list_students(students)
                └─► build summary dicts for each student
Back to AdminPage:
  print "Student List"
  for each student: name, ID, and email
```

### **Flow Summary**
- **Controller** loads all students.
- **Model (Admin)**:
  - Builds a summary dictionary for each student:
    ```python
    {
        "id": s.id,
        "name": s.name,
        "email": s.email,
        "subjects_count": len(s.subjects),
        "avg": round(avg, 2),
        "grade": overall_grade_for(s)
    }
    ```
- **View** prints each student’s info in a clean list.

### **Result**
Displays all students currently in the system.

---

# 🧠 Summary Table

| Command | Description | Controller Action | Model Role | Database Interaction | View Output |
|----------|--------------|------------------|-------------|----------------------|--------------|
| **c** | Clear DB | `_write_students([])` | — | Overwrite file with `[]` | “Students data cleared” |
| **g** | Group by Grade | `group_by_grade()` | Compute grades | Read only | Groups by HD–F |
| **p** | Pass/Fail Split | `partition_pass_fail()` | avg ≥ 50 → PASS else FAIL | Read only | FAIL → PASS lists |
| **r** | Remove Student | `remove_student_by_id()` | Filter by ID | Read → Write | Removal success/fail |
| **s** | Show All | `list_students()` | Build summary dicts | Read only | Prints full student list |
