import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
import sqlite3

def initialize_db():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            department TEXT NOT NULL,
            phone TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            address TEXT,
            phone TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id INTEGER NOT NULL,
            patient_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (doctor_id) REFERENCES doctors(id),
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    ''')
    conn.commit()
    conn.close()

class HospitalSystemGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Hospital Management System")
        self.master.geometry("800x600")

        self.menu_label = tk.Label(master, text="Hospital Management System Menu", font=("Arial", 18, "bold"))
        self.menu_label.pack(pady=20)

        self.choices = [
            ("Add a doctor", self.add_doctor),
            ("Add a patient", self.add_patient),
            ("Remove a doctor", self.remove_doctor),
            ("Remove a patient", self.remove_patient),
            ("View all patients", self.view_all_patients),
            ("Schedule appointment", self.schedule_appointment),
            ("Cancel appointment", self.cancel_appointment),
            ("View appointments", self.view_appointments),
            ("Exit", self.master.destroy)
        ]

        for choice_text, command in self.choices:
            btn = tk.Button(master, text=choice_text, command=command, bg="#008CBA", fg="white", font=("Arial", 12), padx=10, pady=5)
            btn.pack(fill=tk.X, padx=20, pady=5)

        self.tree = ttk.Treeview(master, columns=("Position", "Department"))
        self.tree.heading("#0", text="Name")
        self.tree.heading("Position", text="Position")
        self.tree.heading("Department", text="Department")
        self.tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

    def add_doctor(self):
        name = simpledialog.askstring("Add a Doctor", "Enter doctor's name:")
        position = simpledialog.askstring("Add a Doctor", "Enter doctor's position:")
        department = simpledialog.askstring("Add a Doctor", "Enter doctor's department:")
        phone = simpledialog.askstring("Add a Doctor", "Enter doctor's phone (optional):")
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO doctors (name, position, department, phone) VALUES (?, ?, ?, ?)', (name, position, department, phone))
        conn.commit()
        conn.close()
        self.update_treeview()

    def add_patient(self):
        name = simpledialog.askstring("Add a Patient", "Enter patient's name:")
        age = simpledialog.askinteger("Add a Patient", "Enter patient's age:")
        gender = simpledialog.askstring("Add a Patient", "Enter patient's gender:")
        address = simpledialog.askstring("Add a Patient", "Enter patient's address (optional):")
        phone = simpledialog.askstring("Add a Patient", "Enter patient's phone (optional):")
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO patients (name, age, gender, address, phone) VALUES (?, ?, ?, ?, ?)', (name, age, gender, address, phone))
        conn.commit()
        conn.close()

    def remove_doctor(self):
        doctor_id = simpledialog.askinteger("Remove a Doctor", "Enter doctor's ID:")
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM doctors WHERE id = ?', (doctor_id,))
        conn.commit()
        conn.close()
        self.update_treeview()

    def remove_patient(self):
        patient_id = simpledialog.askinteger("Remove a Patient", "Enter patient's ID:")
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
        conn.commit()
        conn.close()

    def view_all_patients(self):
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM patients')
        patients = cursor.fetchall()
        conn.close()
        messagebox.showinfo("All Patients", patients)

    def schedule_appointment(self):
        doctor_name = simpledialog.askstring("Schedule Appointment", "Enter doctor's name:")
        patient_name = simpledialog.askstring("Schedule Appointment", "Enter patient's name:")
        date = simpledialog.askstring("Schedule Appointment", "Enter appointment date (YYYY-MM-DD):")
        time = simpledialog.askstring("Schedule Appointment", "Enter appointment time:")
        notes = simpledialog.askstring("Schedule Appointment", "Enter notes (optional):")
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM doctors WHERE name = ?', (doctor_name,))
        doctor_id = cursor.fetchone()[0]
        cursor.execute('SELECT id FROM patients WHERE name = ?', (patient_name,))
        patient_id = cursor.fetchone()[0]
        cursor.execute('INSERT INTO appointments (doctor_id, patient_id, date, time, notes) VALUES (?, ?, ?, ?, ?)', (doctor_id, patient_id, date, time, notes))
        conn.commit()
        conn.close()

    def cancel_appointment(self):
        patient_id = simpledialog.askinteger("Cancel Appointment", "Enter patient's ID:")
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM appointments WHERE patient_id = ?', (patient_id,))
        conn.commit()
        conn.close()

    def view_appointments(self):
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT doctors.name, appointments.date, appointments.time, patients.name, appointments.notes
            FROM appointments
            INNER JOIN doctors ON appointments.doctor_id = doctors.id
            INNER JOIN patients ON appointments.patient_id = patients.id
        ''')
        appointments = cursor.fetchall()
        conn.close()
        messagebox.showinfo("Appointments", appointments)

    def update_treeview(self):
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, position, department FROM doctors')
        doctors = cursor.fetchall()
        for doctor in doctors:
            self.tree.insert("", "end", text=doctor[0], values=(doctor[1], doctor[2]))
        conn.close()

def main():
    initialize_db()
    root = tk.Tk()
    root.configure(bg="#f0f0f0")  # Background color
    app = HospitalSystemGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
