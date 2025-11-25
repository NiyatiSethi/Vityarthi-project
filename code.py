import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import sqlite3

def get_connection():
    base_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_path, "faculty.db")
    return sqlite3.connect(db_path)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faculty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            qualification TEXT NOT NULL,
            experience INTEGER NOT NULL
        );
    """)
    conn.commit()
    conn.close()

# CRUD Functions
def add_faculty(name, department, qualification, experience):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO faculty (name, department, qualification, experience) VALUES (?, ?, ?, ?)",
        (name, department, qualification, experience)
    )
    conn.commit()
    conn.close()

def get_all_faculty():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM faculty")
    rows = cursor.fetchall()

    conn.close()
    return rows

def update_faculty(fid, name, department, qualification, experience):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """UPDATE faculty
           SET name = ?, department = ?, qualification = ?, experience = ?
           WHERE id = ?""",
        (name, department, qualification, experience, fid)
    )
    conn.commit()
    conn.close()

def delete_faculty(fid):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM faculty WHERE id = ?", (fid,))
    conn.commit()
    conn.close()


# GUI Application
def start_app():
    root = tk.Tk()
    root.title("Faculty Data Manager")
    root.geometry("1000x500")

    top_frame = tk.Frame(root)
    top_frame.pack(pady=10)

    tk.Label(top_frame, text="Name").grid(row=0, column=0)
    name_entry = tk.Entry(top_frame)
    name_entry.grid(row=0, column=1, padx=5)

    tk.Label(top_frame, text="Department").grid(row=1, column=0)
    dept_entry = tk.Entry(top_frame)
    dept_entry.grid(row=1, column=1, padx=5)

    tk.Label(top_frame, text="Qualification").grid(row=2, column=0)
    qual_entry = tk.Entry(top_frame)
    qual_entry.grid(row=2, column=1, padx=5)

    tk.Label(top_frame, text="Experience").grid(row=3, column=0)
    exp_entry = tk.Entry(top_frame)
    exp_entry.grid(row=3, column=1, padx=5)

    message = tk.Label(root, text="", fg="red")
    message.pack()

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    selected_id = None

   
    # Save new record
    def save_record():
        name = name_entry.get().strip()
        dept = dept_entry.get().strip()
        qual = qual_entry.get().strip()
        exp = exp_entry.get().strip()

        if not name or not dept or not qual or not exp:
            message.config(text="All fields are required", fg="red")
            return
        
        if any(char.isdigit() for char in name):
            message.config(text="Name cannot contain numbers", fg="red")
            return

        if not exp.isdigit():
            message.config(text="Experience must be a number", fg="red")
            return

        add_faculty(name, dept, qual, exp)
        load_records()
        message.config(text="Record added successfully!", fg="green")

    tk.Button(btn_frame, text="Add Faculty", width=15, command=save_record).grid(row=0, column=0, padx=10)

    # Table
    columns = ("id", "name", "dept", "qual", "exp")
    table = ttk.Treeview(root, columns=columns, show="headings")

    for col in columns:
        table.heading(col, text=col.title())

    table.pack(fill="both", expand=True, pady=10)


    def load_records():
        table.delete(*table.get_children())
        for item in get_all_faculty():
            table.insert("", tk.END, values=item)

    load_records()

    # Row Selection
    def select_row(event):
        nonlocal selected_id
        current = table.focus()

        if current:
            values = table.item(current, "values")
            if values:
                selected_id = int(values[0])  

                name_entry.delete(0, tk.END)
                dept_entry.delete(0, tk.END)
                qual_entry.delete(0, tk.END)
                exp_entry.delete(0, tk.END)

                name_entry.insert(0, values[1])
                dept_entry.insert(0, values[2])
                qual_entry.insert(0, values[3])
                exp_entry.insert(0, values[4])

    table.bind("<<TreeviewSelect>>", select_row)

    # Update a record
    def update_record():
        if selected_id is None:
            message.config(text="Please select a record to update", fg="red")
            return

        name = name_entry.get().strip()
        dept = dept_entry.get().strip()
        qual = qual_entry.get().strip()
        exp = exp_entry.get().strip()

        if not name or not dept or not qual or not exp:
            message.config(text="Please fill all fields before updating", fg="red")
            return

        if any(char.isdigit() for char in name):
            message.config(text="Name cannot contain numbers", fg="red")
            return

        if not exp.isdigit():
            message.config(text="Experience must be a number", fg="red")
            return

        update_faculty(selected_id, name, dept, qual, exp)
        load_records()
        message.config(text="Record updated successfully!", fg="green")

    tk.Button(btn_frame, text="Update Faculty", width=15, command=update_record).grid(row=0, column=1, padx=10)

    # Deleting a record
    def delete_record():
        nonlocal selected_id
        if selected_id is None:
            message.config(text="Please select a record to delete", fg="red")
            return

        delete_faculty(selected_id)
        load_records()

        name_entry.delete(0, tk.END)
        dept_entry.delete(0, tk.END)
        qual_entry.delete(0, tk.END)
        exp_entry.delete(0, tk.END)

        selected_id = None
        message.config(text="Record deleted successfully!", fg="green")

    tk.Button(btn_frame, text="Delete Faculty", width=15, command=delete_record).grid(row=0, column=2, padx=10)

    root.mainloop()


create_table()
print("Faculty Data CRUD Manager started.")
start_app()