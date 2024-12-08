# Import CSV  and JSON 
import csv
import json

# Create a list that will store the student records
Student_Records = []

# Create a function that will add a student to the student record system
def add_student():
    """Adds a new student record with subjects and grades."""
    try:
        Student_ID = input("Enter student ID: ")
        Name = input("Enter student name: ")
        Course = input("Enter student course: ")
        Grades = {}
        while True:
            subject = input("Enter subject name (or type 'done'): ")
            if subject.lower() == 'done':
                break
            while True:
                try:
                    grade = float(input(f"Enter grade for {subject} (0.0-100.0): "))
                    if 0.0 <= grade <= 100.0:
                        Grades[subject] = grade
                        break
                    else:
                        print("Grade must be between 0.0 and 100.0")
                except ValueError:
                    print("Invalid grade. Please enter a numeric value.")
        Student_Records.append({"Student_ID": Student_ID, "Name": Name, "Course": Course, "Grades": Grades})
        print("Student record added successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")


# Create a function that wiil search a student by ID
def search_student():
    """Searches for a student record by ID and displays it in a table-like format."""
    student_id = input("Enter student ID to search for: ")
    for record in Student_Records:
        if record["Student_ID"] == student_id:
            print("Student Found:")
            # Table-like display 
            col_widths = {
                "Student_ID": len("Student ID"),
                "Name": len("Name"),
                "Course": len("Course"),
            }
            for key, value in record.items():
                if key == "Grades":
                    for subject, grade in value.items():
                        col_widths[subject] = max(col_widths.get(subject, 0), len(subject))
                else:
                    col_widths[key] = max(col_widths.get(key, 0), len(str(value)))

            header_row = "{:<{}}|{:<{}}|{:<{}}".format("Student ID", col_widths["Student_ID"], 
                                                       "Name", col_widths["Name"], "Course", col_widths["Course"])
            for subject in col_widths:
                if subject != "Student_ID" and subject != "Name" and subject != "Course":
                    header_row += "| {:<{}}".format(subject, col_widths[subject])
            print(header_row)
            print("-" * len(header_row))

            row = "{:<{}}|{:<{}}|{:<{}}".format(record["Student_ID"], col_widths["Student_ID"],
             record["Name"], col_widths["Name"], record["Course"], col_widths["Course"])
            for subject in col_widths:
                if subject != "Student_ID" and subject != "Name" and subject != "Course":
                    row += "| {:<{}}".format(record["Grades"].get(subject, ""), col_widths[subject])
            print(row)
            #  End of table-like display 
            return
    print("Student not found.")


# Create a function that will save student records
def save_records():
    """Saves student records to a CSV file."""
    try:
        with open("Student_Records.csv", "w", newline="") as csvfile:
            fieldnames = ["Student_ID", "Name", "Course", "Grades"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for record in Student_Records:
                # Convert the Grades dictionary to a JSON string
                record["Grades"] = json.dumps(record["Grades"])
                writer.writerow(record)
        print("Records saved to Student_Records.csv")
    except Exception as e:
        print(f"An error occurred while saving: {e}")

def load_records():
    """Loads student records from a CSV file, handling Grades as JSON strings."""
    try:
        with open("student_records.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert the 'Grades' string to a dictionary using json.loads()
                row['Grades'] = json.loads(row['Grades'])
                Student_Records.append(row)
        print("Records loaded from student_records.csv")
    except FileNotFoundError:
        print("student_records.csv not found. Starting with an empty database.")
    except (json.JSONDecodeError, Exception) as e:
        print(f"An error occurred while loading: {e}")

# Create a function that will display the student records
def display_records():
    """Displays all student records in a rudimentary tabular format."""
    if not Student_Records:
        print("No student records found.")
        return

    col_widths = {
        "Student_ID": len("Student ID"),
        "Name": len("Name"),
        "Course": len("Course"),
    }
    all_subjects = set()
    for record in Student_Records:
        all_subjects.update(record['Grades'].keys())
    for subject in all_subjects:
        col_widths[subject] = len(subject)
    for record in Student_Records:
        for key, value in record.items():
            if key == "Grades":
                for subject, grade in value.items():
                    col_widths[subject] = max(col_widths.get(subject, 0), len(str(grade)))
            else:
                col_widths[key] = max(col_widths.get(key, 0), len(str(value)))

    header_row = "{:<{}}|{:<{}}|{:<{}}".format("Student ID", col_widths["Student_ID"], 
                                               "Name", col_widths["Name"], "Course", col_widths["Course"])
    for subject in all_subjects:
        header_row += "| {:<{}}".format(subject, col_widths[subject])
    print(header_row)
    print("-" * len(header_row))

    for record in Student_Records:
        row = "{:<{}}|{:<{}}|{:<{}}".format(record["Student_ID"], col_widths["Student_ID"],
                                             record["Name"], col_widths["Name"], record["Course"], col_widths["Course"])
        for subject in all_subjects:
            row += "| {:<{}}".format(record["Grades"].get(subject, ""), col_widths[subject])
        print(row)


# Create a function that will delete a student record by ID
def delete_student():
    student_id = input("Enter student ID to delete: ")
    for i, record in enumerate(Student_Records):
        if record["Student_ID"] == student_id:
            del Student_Records[i]
            print("Student record deleted.")
            return
    print("Student not found.")


# Main program loop
load_records()

while True:
    print("\nHello I'm Suga! Welcome to GK Student Record Menu")
    print("1. Add Student")
    print("2. Search Student")
    print("3. Save Records")
    print("4. Display All Records")
    print("5. Delete Student")
    print("6. Exit")

    choice = input("Please enter your choice: ")

    if choice == "1":
        add_student()
    elif choice == "2":
        search_student()
    elif choice == "3":
        save_records()
    elif choice == "4":
        display_records()
    elif choice == "5":
        delete_student()
    elif choice == "6":
        break
    else:
        print("Invalid choice. Please try again.")

print("Exiting Student Record System.")  