import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip


# ---------------- PASSWORD GENERATOR ---------------- #

AMBIGUOUS = "0Ol1"

def generate_password():
    try:
        length = int(length_var.get())
    except ValueError:
        messagebox.showerror("Invalid Length", "Please enter a valid password length.")
        return

    if length < 8:
        messagebox.showerror(
            "Invalid Length",
            "Password length must be at least 8 characters."
        )
        return

    selected_types = []

    if uppercase_var.get():
        selected_types.append(string.ascii_uppercase)

    if lowercase_var.get():
        selected_types.append(string.ascii_lowercase)

    if numbers_var.get():
        selected_types.append(string.digits)

    if symbols_var.get():
        selected_types.append(string.punctuation)

    if len(selected_types) < 2:
        messagebox.showwarning(
            "Character Types",
            "Please select at least 2 character types."
        )
        return

    # Remove ambiguous characters if selected
    if exclude_var.get():
        selected_types = [
            ''.join(char for char in chars if char not in AMBIGUOUS)
            for chars in selected_types
        ]

    # Make sure no selected type became empty
    selected_types = [chars for chars in selected_types if chars]

    if len(selected_types) < 2:
        messagebox.showwarning(
            "Character Types",
            "Not enough characters available after excluding ambiguous characters."
        )
        return

    # Guarantee at least one character from every selected type
    password_chars = [
        secrets.choice(chars)
        for chars in selected_types
    ]

    all_characters = ''.join(selected_types)

    # Fill remaining characters
    while len(password_chars) < length:
        password_chars.append(secrets.choice(all_characters))

    # Secure shuffle
    for i in range(len(password_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_chars[i], password_chars[j] = (
            password_chars[j],
            password_chars[i]
        )

    password = ''.join(password_chars)

    password_var.set(password)

    # Copy automatically
    pyperclip.copy(password)

    # Add to history
    history.insert(0, password)

    if len(history) > 5:
        history.pop()

    update_history()
    update_strength(password)


# ---------------- STRENGTH ---------------- #

def update_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1

    if len(password) >= 12:
        score += 1

    if any(c.isupper() for c in password):
        score += 1

    if any(c.islower() for c in password):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(c in string.punctuation for c in password):
        score += 1

    if score <= 2:
        strength_var.set("Weak")
    elif score <= 4:
        strength_var.set("Medium")
    else:
        strength_var.set("Strong")


# ---------------- COPY ---------------- #

def copy_password():
    password = password_var.get()

    if password:
        pyperclip.copy(password)
        messagebox.showinfo(
            "Copied",
            "Password copied to clipboard!"
        )
    else:
        messagebox.showwarning(
            "No Password",
            "Generate a password first."
        )


# ---------------- HISTORY ---------------- #

def update_history():
    history_box.delete(0, tk.END)

    for password in history:
        history_box.insert(tk.END, password)


# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Secure Password Generator")
root.geometry("650x700")
root.resizable(False, False)

# Variables
length_var = tk.StringVar(value="16")
uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)
exclude_var = tk.BooleanVar(value=False)

password_var = tk.StringVar()
strength_var = tk.StringVar(value="Strength: -")

history = []


# Title
title = tk.Label(
    root,
    text="Secure Password Generator",
    font=("Arial", 24, "bold")
)
title.pack(pady=(25, 5))

subtitle = tk.Label(
    root,
    text="Create strong and secure passwords",
    font=("Arial", 11)
)
subtitle.pack(pady=(0, 20))


# Password display
password_entry = tk.Entry(
    root,
    textvariable=password_var,
    font=("Consolas", 18),
    justify="center",
    width=38
)
password_entry.pack(pady=10)


# Strength
strength_label = tk.Label(
    root,
    textvariable=strength_var,
    font=("Arial", 13, "bold")
)
strength_label.pack(pady=5)


# Length
length_frame = tk.Frame(root)
length_frame.pack(pady=15)

tk.Label(
    length_frame,
    text="Password Length:",
    font=("Arial", 12)
).pack(side="left", padx=10)

length_spinbox = tk.Spinbox(
    length_frame,
    from_=8,
    to=100,
    textvariable=length_var,
    width=8,
    font=("Arial", 12)
)
length_spinbox.pack(side="left")


# Character types
options_frame = tk.LabelFrame(
    root,
    text="Character Types",
    font=("Arial", 12, "bold"),
    padx=15,
    pady=10
)
options_frame.pack(padx=40, fill="x")

tk.Checkbutton(
    options_frame,
    text="Uppercase Letters (A-Z)",
    variable=uppercase_var,
    font=("Arial", 11)
).pack(anchor="w")

tk.Checkbutton(
    options_frame,
    text="Lowercase Letters (a-z)",
    variable=lowercase_var,
    font=("Arial", 11)
).pack(anchor="w")

tk.Checkbutton(
    options_frame,
    text="Numbers (0-9)",
    variable=numbers_var,
    font=("Arial", 11)
).pack(anchor="w")

tk.Checkbutton(
    options_frame,
    text="Symbols (!@#$...)",
    variable=symbols_var,
    font=("Arial", 11)
).pack(anchor="w")


# Exclude ambiguous
tk.Checkbutton(
    root,
    text="Exclude ambiguous characters (0, O, l, 1)",
    variable=exclude_var,
    font=("Arial", 11)
).pack(pady=15)


# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

generate_button = tk.Button(
    button_frame,
    text="Generate Password",
    command=generate_password,
    font=("Arial", 12, "bold"),
    padx=20,
    pady=8
)
generate_button.pack(side="left", padx=8)

copy_button = tk.Button(
    button_frame,
    text="Copy to Clipboard",
    command=copy_password,
    font=("Arial", 12, "bold"),
    padx=20,
    pady=8
)
copy_button.pack(side="left", padx=8)


# History
history_frame = tk.LabelFrame(
    root,
    text="Last 5 Generated Passwords",
    font=("Arial", 12, "bold"),
    padx=10,
    pady=10
)
history_frame.pack(
    padx=40,
    pady=20,
    fill="both"
)

history_box = tk.Listbox(
    history_frame,
    height=5,
    font=("Consolas", 11)
)
history_box.pack(fill="both")


# Footer
tk.Label(
    root,
    text="Passwords are generated securely using Python's secrets module.",
    font=("Arial", 9)
).pack(pady=10)


root.mainloop()
