import tkinter as tk
from tkinter import messagebox
import sqlite3
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Database setup
conn = sqlite3.connect('bmi_history.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                weight REAL,
                height REAL,
                bmi REAL,
                category TEXT)''')
conn.commit()

# Function to calculate BMI
def calculate_bmi(weight, height):
    return weight / (height ** 2)

# Function to classify BMI
def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

# Function to handle the calculate button click
def on_calculate():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        if weight <= 0 or height <= 0:
            raise ValueError

        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)

        result_label.config(text=f"Your BMI is {bmi:.2f}\nCategory: {category}")

        # Save to database
        c.execute('INSERT INTO bmi_records (weight, height, bmi, category) VALUES (?, ?, ?, ?)',
                  (weight, height, bmi, category))
        conn.commit()
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid positive numbers for weight and height.")

# Function to show historical data
def show_history():
    c.execute('SELECT * FROM bmi_records')
    records = c.fetchall()

    if not records:
        messagebox.showinfo("No data", "No historical data available.")
        return

    weights, heights, bmis = zip(*[(rec[1], rec[2], rec[3]) for rec in records])
    
    fig, ax = plt.subplots()
    ax.plot(range(len(bmis)), bmis, marker='o')
    ax.set_title("BMI History")
    ax.set_xlabel("Entry Number")
    ax.set_ylabel("BMI")

    canvas = FigureCanvasTkAgg(fig, master=history_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

# GUI setup
root = tk.Tk()
root.title("BMI Calculator")

tk.Label(root, text="Weight (kg):").grid(row=0, column=0)
weight_entry = tk.Entry(root)
weight_entry.grid(row=0, column=1)

tk.Label(root, text="Height (m):").grid(row=1, column=0)
height_entry = tk.Entry(root)
height_entry.grid(row=1, column=1)

calculate_button = tk.Button(root, text="Calculate BMI", command=on_calculate)
calculate_button.grid(row=2, columnspan=2)

result_label = tk.Label(root, text="Your BMI will be shown here.")
result_label.grid(row=3, columnspan=2)

history_button = tk.Button(root, text="Show History", command=show_history)
history_button.grid(row=4, columnspan=2)

history_window = tk.Toplevel(root)
history_window.withdraw()
history_window.title("BMI History")

root.mainloop()

conn.close()
