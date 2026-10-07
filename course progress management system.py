import tkinter as tk
from tkinter import messagebox
import sqlite3


# ---------------- DATABASE ----------------

conn = sqlite3.connect("course_management.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    total_lessons INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER,
    lesson_name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    lesson_id INTEGER,
    UNIQUE(student_id, lesson_id)
)
""")

conn.commit()


# ---------------- SAMPLE COURSES ----------------

cursor.execute("SELECT COUNT(*) FROM courses")
course_count = cursor.fetchone()[0]

if course_count == 0:

    courses = [
        ("Python Programming",
         "Learn Python from basics",
         5),

        ("Java Programming",
         "Learn Java programming",
         5),

        ("Data Structures",
         "Learn basic data structures",
         5)
    ]

    cursor.executemany("""
    INSERT INTO courses
    (name, description, total_lessons)
    VALUES (?, ?, ?)
    """, courses)

    conn.commit()

    # Python Lessons
    cursor.execute("SELECT id FROM courses WHERE name='Python Programming'")
    python_id = cursor.fetchone()[0]

    python_lessons = [
        (python_id, "Introduction to Python"),
        (python_id, "Variables"),
        (python_id, "If Else"),
        (python_id, "Loops"),
        (python_id, "Functions")
    ]

    # Java Lessons
    cursor.execute("SELECT id FROM courses WHERE name='Java Programming'")
    java_id = cursor.fetchone()[0]

    java_lessons = [
        (java_id, "Introduction to Java"),
        (java_id, "Variables"),
        (java_id, "Conditions"),
        (java_id, "Loops"),
        (java_id, "Classes and Objects")
    ]

    # DSA Lessons
    cursor.execute("SELECT id FROM courses WHERE name='Data Structures'")
    dsa_id = cursor.fetchone()[0]

    dsa_lessons = [
        (dsa_id, "Introduction to Data Structures"),
        (dsa_id, "Array"),
        (dsa_id, "Stack"),
        (dsa_id, "Queue"),
        (dsa_id, "Linked List")
    ]

    cursor.executemany("""
    INSERT INTO lessons
    (course_id, lesson_name)
    VALUES (?, ?)
    """, python_lessons + java_lessons + dsa_lessons)

    conn.commit()


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Online Course Progress Management System")
root.geometry("700x600")


current_student = None


# ---------------- CLEAR SCREEN ----------------

def clear_screen():

    for widget in root.winfo_children():
        widget.destroy()


# ---------------- REGISTRATION ----------------

def registration():

    clear_screen()

    tk.Label(
        root,
        text="Student Registration",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    tk.Label(root, text="Name").pack()
    name_entry = tk.Entry(root, width=35)
    name_entry.pack(pady=5)

    tk.Label(root, text="Email").pack()
    email_entry = tk.Entry(root, width=35)
    email_entry.pack(pady=5)

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(
        root,
        width=35,
        show="*"
    )
    password_entry.pack(pady=5)

    def register_student():

        name = name_entry.get()
        email = email_entry.get()
        password = password_entry.get()

        if name == "" or email == "" or password == "":
            messagebox.showwarning(
                "Warning",
                "Please fill all fields"
            )
            return

        try:

            cursor.execute("""
            INSERT INTO students
            (name, email, password)
            VALUES (?, ?, ?)
            """, (name, email, password))

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Registration Successful!"
            )

            login()

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Error",
                "Email already registered"
            )

    tk.Button(
        root,
        text="Register",
        width=20,
        command=register_student
    ).pack(pady=15)

    tk.Button(
        root,
        text="Back to Login",
        width=20,
        command=login
    ).pack()


# ---------------- LOGIN ----------------

def login():

    clear_screen()

    tk.Label(
        root,
        text="Student Login",
        font=("Arial", 22, "bold")
    ).pack(pady=30)

    tk.Label(root, text="Email").pack()

    email_entry = tk.Entry(
        root,
        width=35
    )
    email_entry.pack(pady=5)

    tk.Label(root, text="Password").pack()

    password_entry = tk.Entry(
        root,
        width=35,
        show="*"
    )
    password_entry.pack(pady=5)

    def login_student():

        global current_student

        email = email_entry.get()
        password = password_entry.get()

        cursor.execute("""
        SELECT id, name
        FROM students
        WHERE email=? AND password=?
        """, (email, password))

        student = cursor.fetchone()

        if student:

            current_student = student

            messagebox.showinfo(
                "Success",
                "Login Successful!"
            )

            dashboard()

        else:

            messagebox.showerror(
                "Error",
                "Invalid Email or Password"
            )

    tk.Button(
        root,
        text="Login",
        width=20,
        command=login_student
    ).pack(pady=15)

    tk.Button(
        root,
        text="Create New Account",
        width=20,
        command=registration
    ).pack()


# ---------------- DASHBOARD ----------------

def dashboard():

    clear_screen()

    tk.Label(
        root,
        text="Student Dashboard",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    tk.Label(
        root,
        text="Welcome " + current_student[1],
        font=("Arial", 15)
    ).pack(pady=10)

    tk.Button(
        root,
        text="View Courses",
        width=30,
        height=2,
        command=view_courses
    ).pack(pady=10)

    tk.Button(
        root,
        text="My Courses",
        width=30,
        height=2,
        command=my_courses
    ).pack(pady=10)

    tk.Button(
        root,
        text="Logout",
        width=30,
        height=2,
        command=login
    ).pack(pady=10)


# ---------------- VIEW COURSES ----------------

def view_courses():

    clear_screen()

    tk.Label(
        root,
        text="Available Courses",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    cursor.execute("""
    SELECT id, name, description, total_lessons
    FROM courses
    """)

    courses = cursor.fetchall()

    for course in courses:

        frame = tk.Frame(
            root,
            bd=2,
            relief="solid",
            padx=10,
            pady=10
        )

        frame.pack(
            fill="x",
            padx=30,
            pady=8
        )

        tk.Label(
            frame,
            text=course[1],
            font=("Arial", 15, "bold")
        ).pack()

        tk.Label(
            frame,
            text=course[2]
        ).pack()

        tk.Label(
            frame,
            text="Total Lessons: " +
                 str(course[3])
        ).pack()

        tk.Button(
            frame,
            text="Enroll",
            command=lambda c=course[0]:
            enroll_course(c)
        ).pack(pady=5)

    tk.Button(
        root,
        text="Back",
        command=dashboard
    ).pack(pady=15)


# ---------------- ENROLL COURSE ----------------

def enroll_course(course_id):

    cursor.execute("""
    SELECT id
    FROM enrollments
    WHERE student_id=? AND course_id=?
    """,
    (current_student[0], course_id))

    already = cursor.fetchone()

    if already:

        messagebox.showinfo(
            "Information",
            "You are already enrolled"
        )

        return

    cursor.execute("""
    INSERT INTO enrollments
    (student_id, course_id)
    VALUES (?, ?)
    """,
    (current_student[0], course_id))

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Course Enrolled Successfully!"
    )


# ---------------- MY COURSES ----------------

def my_courses():

    clear_screen()

    tk.Label(
        root,
        text="My Courses",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    cursor.execute("""
    SELECT courses.id,
           courses.name,
           courses.total_lessons
    FROM courses
    JOIN enrollments
    ON courses.id = enrollments.course_id
    WHERE enrollments.student_id=?
    """,
    (current_student[0],))

    courses = cursor.fetchall()

    if not courses:

        tk.Label(
            root,
            text="No courses enrolled yet"
        ).pack(pady=20)

    for course in courses:

        course_id = course[0]

        cursor.execute("""
        SELECT COUNT(*)
        FROM lessons
        WHERE course_id=?
        """, (course_id,))

        total = cursor.fetchone()[0]

        cursor.execute("""
        SELECT COUNT(*)
        FROM progress
        JOIN lessons
        ON progress.lesson_id = lessons.id
        WHERE progress.student_id=?
        AND lessons.course_id=?
        """,
        (current_student[0], course_id))

        completed = cursor.fetchone()[0]

        if total > 0:

            percent = (completed / total) * 100

        else:

            percent = 0

        frame = tk.Frame(
            root,
            bd=2,
            relief="solid",
            padx=15,
            pady=10
        )

        frame.pack(
            fill="x",
            padx=30,
            pady=8
        )

        tk.Label(
            frame,
            text=course[1],
            font=("Arial", 15, "bold")
        ).pack()

        tk.Label(
            frame,
            text="Progress: " +
                 str(round(percent, 2)) +
                 "%"
        ).pack()

        if percent == 100:

            status = "Completed"

        else:

            status = "In Progress"

        tk.Label(
            frame,
            text="Status: " + status
        ).pack()

        tk.Button(
            frame,
            text="Open Course",
            command=lambda c=course_id:
            open_course(c)
        ).pack(pady=5)

    tk.Button(
        root,
        text="Back",
        command=dashboard
    ).pack(pady=15)


# ---------------- OPEN COURSE ----------------

def open_course(course_id):

    clear_screen()

    cursor.execute("""
    SELECT name
    FROM courses
    WHERE id=?
    """,
    (course_id,))

    course = cursor.fetchone()

    tk.Label(
        root,
        text=course[0],
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    cursor.execute("""
    SELECT id, lesson_name
    FROM lessons
    WHERE course_id=?
    """,
    (course_id,))

    lessons = cursor.fetchall()

    for lesson in lessons:

        lesson_id = lesson[0]

        cursor.execute("""
        SELECT id
        FROM progress
        WHERE student_id=? AND lesson_id=?
        """,
        (current_student[0], lesson_id))

        completed = cursor.fetchone()

        frame = tk.Frame(
            root,
            bd=1,
            relief="solid",
            padx=10,
            pady=8
        )

        frame.pack(
            fill="x",
            padx=40,
            pady=5
        )

        tk.Label(
            frame,
            text=lesson[1],
            font=("Arial", 13)
        ).pack(side="left")

        if completed:

            tk.Label(
                frame,
                text="Completed"
            ).pack(side="right")

        else:

            tk.Button(
                frame,
                text="Complete",
                command=lambda l=lesson_id,
                c=course_id:
                complete_lesson(l, c)
            ).pack(side="right")

    tk.Button(
        root,
        text="Back",
        command=my_courses
    ).pack(pady=20)


# ---------------- COMPLETE LESSON ----------------

def complete_lesson(lesson_id, course_id):

    cursor.execute("""
    INSERT INTO progress
    (student_id, lesson_id)
    VALUES (?, ?)
    """,
    (current_student[0], lesson_id))

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Lesson Completed!"
    )

    open_course(course_id)


# ---------------- START ----------------

login()

root.mainloop()

conn.close()