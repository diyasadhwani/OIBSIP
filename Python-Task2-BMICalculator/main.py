import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt


def create_database():
    try:
        connection = sqlite3.connect("bmi_database.db")
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)

        connection.commit()
        connection.close()

    except sqlite3.Error:
        messagebox.showerror(
            "Database Error",
            "Could not create the database."
        )

def calculate_bmi():
    try:
        name = name_entry.get().strip()
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if not name:
            messagebox.showerror(
                "Invalid Input",
                "Please enter your name."
            )
            return

        if weight <= 0 or height <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Weight and height must be greater than 0."
            )
            return

        bmi = weight / (height ** 2)

        if bmi < 18.5:
            category = "Underweight"
            result_color = "#2563EB"

        elif bmi < 25:
            category = "Normal"
            result_color = "#16A34A"

        elif bmi < 30:
            category = "Overweight"
            result_color = "#EA580C"

        else:
            category = "Obese"
            result_color = "#DC2626"

        current_date = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        connection = sqlite3.connect("bmi_database.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO bmi_records
            (name, weight, height, bmi, category, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            weight,
            height,
            bmi,
            category,
            current_date
        ))

        connection.commit()
        connection.close()

        result_value.config(
            text=f"{bmi:.2f}"
        )

        result_category.config(
            text=category,
            fg=result_color
        )

        result_name.config(
            text=f"{name}'s BMI Result"
        )

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numbers for weight and height."
        )

    except sqlite3.Error:
        messagebox.showerror(
            "Database Error",
            "Could not save the BMI record."
        )



def show_history():
    name = name_entry.get().strip()

    if not name:
        messagebox.showerror(
            "Input Required",
            "Please enter a name first."
        )
        return

    try:
        connection = sqlite3.connect("bmi_database.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT bmi, date
            FROM bmi_records
            WHERE name = ?
            ORDER BY date
        """, (name,))

        records = cursor.fetchall()
        connection.close()

        if not records:
            messagebox.showinfo(
                "No Records",
                f"No BMI records found for {name}."
            )
            return

        bmi_values = [record[0] for record in records]
        dates = [record[1] for record in records]

        plt.figure(figsize=(10, 5))

        plt.plot(
            dates,
            bmi_values,
            marker="o",
            linewidth=2
        )

        plt.title(
            f"BMI History - {name}",
            fontsize=16
        )

        plt.xlabel("Date")
        plt.ylabel("BMI")

        plt.xticks(
            rotation=45,
            ha="right"
        )

        plt.grid(
            True,
            alpha=0.3
        )

        plt.tight_layout()
        plt.show()

    except sqlite3.Error:
        messagebox.showerror(
            "Database Error",
            "Could not read BMI history."
        )



def show_all_records():

    try:
        connection = sqlite3.connect("bmi_database.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT name, weight, height, bmi, category, date
            FROM bmi_records
            ORDER BY date DESC
        """)

        records = cursor.fetchall()
        connection.close()

        if not records:
            messagebox.showinfo(
                "No Records",
                "No BMI records available."
            )
            return

        history_window = tk.Toplevel(window)

        history_window.title("BMI Records")
        history_window.geometry("900x600")
        history_window.configure(
            bg="#F8FAFC"
        )

        heading = tk.Label(
            history_window,
            text="BMI Records",
            font=("Segoe UI", 22, "bold"),
            bg="#F8FAFC",
            fg="#111827"
        )

        heading.pack(
            pady=20
        )

        frame = tk.Frame(
            history_window,
            bg="white"
        )

        frame.pack(
            padx=40,
            pady=10,
            fill="both",
            expand=True
        )

        text_box = tk.Text(
            frame,
            font=("Segoe UI", 11),
            bg="white",
            fg="#374151",
            relief="flat",
            padx=20,
            pady=20
        )

        text_box.pack(
            fill="both",
            expand=True
        )

        for record in records:

            name = record[0]
            weight = record[1]
            height = record[2]
            bmi = record[3]
            category = record[4]
            date = record[5]

            text_box.insert(
                tk.END,
                f"Name: {name}\n"
                f"Weight: {weight} kg     "
                f"Height: {height} m\n"
                f"BMI: {bmi:.2f}     "
                f"Category: {category}\n"
                f"Date: {date}\n"
                f"{'─' * 80}\n\n"
            )

        text_box.config(
            state=tk.DISABLED
        )

    except sqlite3.Error:
        messagebox.showerror(
            "Database Error",
            "Could not load BMI records."
        )



def clear_fields():

    name_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)

    result_name.config(
        text="Your BMI Result"
    )

    result_value.config(
        text="--"
    )

    result_category.config(
        text="Enter your details",
        fg="#64748B"
    )

create_database()

window = tk.Tk()

window.title(
    "Advanced BMI Calculator"
)

# Full screen / maximized
window.state("zoomed")

window.configure(
    bg="#F1F5F9"
)



style = ttk.Style()

style.theme_use("clam")

style.configure(
    "TEntry",
    font=("Segoe UI", 13),
    padding=10
)

style.configure(
    "Calculate.TButton",
    font=("Segoe UI", 12, "bold"),
    padding=(25, 12),
    foreground="white",
    background="#4F46E5"
)

style.map(
    "Calculate.TButton",
    background=[
        ("active", "#4338CA")
    ]
)

style.configure(
    "Action.TButton",
    font=("Segoe UI", 11),
    padding=(18, 10),
    foreground="#374151",
    background="#E2E8F0"
)

style.map(
    "Action.TButton",
    background=[
        ("active", "#CBD5E1")
    ]
)


# ================= HEADER =================

header = tk.Frame(
    window,
    bg="#4F46E5",
    height=130
)

header.pack(
    fill="x"
)

header.pack_propagate(False)


title = tk.Label(
    header,
    text="Advanced BMI Calculator",
    font=("Segoe UI", 30, "bold"),
    bg="#4F46E5",
    fg="white"
)

title.pack(
    pady=(25, 2)
)


subtitle = tk.Label(
    header,
    text="Calculate, save and track your BMI progress",
    font=("Segoe UI", 12),
    bg="#4F46E5",
    fg="#E0E7FF"
)

subtitle.pack()


# ================= CONTENT =================

content = tk.Frame(
    window,
    bg="#F1F5F9"
)

content.pack(
    fill="both",
    expand=True,
    padx=70,
    pady=50
)


# ================= LEFT CARD =================

left_card = tk.Frame(
    content,
    bg="white",
    highlightbackground="#E2E8F0",
    highlightthickness=1
)

left_card.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=(0, 25)
)


content.grid_columnconfigure(
    0,
    weight=1
)

content.grid_columnconfigure(
    1,
    weight=1
)

content.grid_rowconfigure(
    0,
    weight=1
)


left_title = tk.Label(
    left_card,
    text="Enter Your Details",
    font=("Segoe UI", 20, "bold"),
    bg="white",
    fg="#111827"
)

left_title.pack(
    anchor="w",
    padx=40,
    pady=(40, 30)
)


# Name

tk.Label(
    left_card,
    text="Name",
    font=("Segoe UI", 11, "bold"),
    bg="white",
    fg="#374151"
).pack(
    anchor="w",
    padx=40
)

name_entry = ttk.Entry(
    left_card
)

name_entry.pack(
    padx=40,
    pady=(7, 25),
    fill="x"
)


# Weight

tk.Label(
    left_card,
    text="Weight (kg)",
    font=("Segoe UI", 11, "bold"),
    bg="white",
    fg="#374151"
).pack(
    anchor="w",
    padx=40
)

weight_entry = ttk.Entry(
    left_card
)

weight_entry.pack(
    padx=40,
    pady=(7, 25),
    fill="x"
)


# Height

tk.Label(
    left_card,
    text="Height (meters)",
    font=("Segoe UI", 11, "bold"),
    bg="white",
    fg="#374151"
).pack(
    anchor="w",
    padx=40
)

height_entry = ttk.Entry(
    left_card
)

height_entry.pack(
    padx=40,
    pady=(7, 30),
    fill="x"
)


calculate_button = ttk.Button(
    left_card,
    text="Calculate BMI",
    command=calculate_bmi,
    style="Calculate.TButton"
)

calculate_button.pack(
    pady=15
)


# ================= RIGHT CARD =================

right_card = tk.Frame(
    content,
    bg="white",
    highlightbackground="#E2E8F0",
    highlightthickness=1
)

right_card.grid(
    row=0,
    column=1,
    sticky="nsew"
)


result_heading = tk.Label(
    right_card,
    text="Your Result",
    font=("Segoe UI", 20, "bold"),
    bg="white",
    fg="#111827"
)

result_heading.pack(
    pady=(45, 15)
)


result_name = tk.Label(
    right_card,
    text="Your BMI Result",
    font=("Segoe UI", 12),
    bg="white",
    fg="#64748B"
)

result_name.pack(
    pady=10
)


result_value = tk.Label(
    right_card,
    text="--",
    font=("Segoe UI", 55, "bold"),
    bg="white",
    fg="#111827"
)

result_value.pack(
    pady=10
)


result_category = tk.Label(
    right_card,
    text="Enter your details",
    font=("Segoe UI", 18, "bold"),
    bg="white",
    fg="#64748B"
)

result_category.pack(
    pady=10
)


info = tk.Label(
    right_card,
    text="Your result will be saved automatically.",
    font=("Segoe UI", 10),
    bg="white",
    fg="#94A3B8"
)

info.pack(
    pady=15
)


# ================= ACTION BUTTONS =================

actions = tk.Frame(
    right_card,
    bg="white"
)

actions.pack(
    pady=35
)


history_button = ttk.Button(
    actions,
    text="BMI History",
    command=show_history,
    style="Action.TButton"
)

history_button.grid(
    row=0,
    column=0,
    padx=7
)


records_button = ttk.Button(
    actions,
    text="All Records",
    command=show_all_records,
    style="Action.TButton"
)

records_button.grid(
    row=0,
    column=1,
    padx=7
)


clear_button = ttk.Button(
    actions,
    text="Clear",
    command=clear_fields,
    style="Action.TButton"
)

clear_button.grid(
    row=0,
    column=2,
    padx=7
)


# ================= FOOTER =================

footer = tk.Label(
    window,
    text="Python • Tkinter • SQLite • Matplotlib",
    font=("Segoe UI", 9),
    bg="#F1F5F9",
    fg="#94A3B8"
)

footer.pack(
    pady=12
)


window.mainloop()