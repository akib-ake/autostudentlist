import tkinter as tk
from tkinter import messagebox
import pandas as pd
import cv2
import os
from datetime import datetime

# Folder for photos
if not os.path.exists("photos"):
    os.makedirs("photos")

# CSV file for storing student info
csv_file = "students_data.csv"
if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=[
        "Student ID", "Name", "Address", "Contact",
        "Guardian Name", "Mother Name", "Father Name", "Photo Path", "Date Added"
    ])
    df.to_csv(csv_file, index=False)

# Function to capture photo
def capture_photo(student_id):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Cannot access the camera!")
        return None

    messagebox.showinfo("Capture", "Press 'SPACE' to take photo, 'ESC' to cancel")
    photo_path = f"photos/{student_id}.jpg"

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Capture Photo", frame)
        key = cv2.waitKey(1)
        if key == 27:  # ESC
            cap.release()
            cv2.destroyAllWindows()
            return None
        elif key == 32:  # SPACE
            cv2.imwrite(photo_path, frame)
            break

    cap.release()
    cv2.destroyAllWindows()
    return photo_path

# Function to save data
def save_data():
    student_id = entry_id.get()
    name = entry_name.get()
    address = entry_address.get()
    contact = entry_contact.get()
    guardian = entry_guardian.get()
    mother = entry_mother.get()
    father = entry_father.get()

    if not student_id or not name:
        messagebox.showerror("Error", "Student ID and Name are required!")
        return

    photo_path = capture_photo(student_id)
    if photo_path is None:
        messagebox.showwarning("Cancelled", "Photo not captured.")
        return

    new_data = pd.DataFrame([{
        "Student ID": student_id,
        "Name": name,
        "Address": address,
        "Contact": contact,
        "Guardian Name": guardian,
        "Mother Name": mother,
        "Father Name": father,
        "Photo Path": photo_path,
        "Date Added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])

    df = pd.read_csv(csv_file)
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(csv_file, index=False)

    messagebox.showinfo("Success", "Student data saved successfully!")
    clear_fields()

# Clear form fields
def clear_fields():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_contact.delete(0, tk.END)
    entry_guardian.delete(0, tk.END)
    entry_mother.delete(0, tk.END)
    entry_father.delete(0, tk.END)

# GUI
root = tk.Tk()
root.title("School Student Manager")
root.geometry("400x400")

tk.Label(root, text="Student ID (Class-Section-Roll)").pack()
entry_id = tk.Entry(root)
entry_id.pack()

tk.Label(root, text="Name").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Address").pack()
entry_address = tk.Entry(root)
entry_address.pack()

tk.Label(root, text="Contact").pack()
entry_contact = tk.Entry(root)
entry_contact.pack()

tk.Label(root, text="Guardian Name").pack()
entry_guardian = tk.Entry(root)
entry_guardian.pack()

tk.Label(root, text="Mother Name").pack()
entry_mother = tk.Entry(root)
entry_mother.pack()

tk.Label(root, text="Father Name").pack()
entry_father = tk.Entry(root)
entry_father.pack()

tk.Button(root, text="Save Student Data", command=save_data).pack(pady=10)

root.mainloop()
# End of the student manager code
# This code creates a simple GUI application to manage student data, including capturing photos and saving the data to a CSV file.