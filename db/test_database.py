from database import Database

# Initilize 
db = Database()

# Make sure the file exists
print("Database file path:", db.path)

# Read current data
print("Initial data:", db.read_from_file())

# Add a test student with password
students = db.read_from_file()

students.append({
    "id": "000001",
    "name": "James",
    "email": "james@university.com",
    "password": "Password123" 
})
db.write_to_file(students)

# Read back the data
print("Data after adding James:", db.read_from_file())

# Clear all data
# db.clear_all()
# print("Data after clear_all():", db.read_from_file())
