from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import json
import os

# ---------------------------- CONSTANTS ------------------------------- #
letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
           'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
numbers = ['0','1','2','3','4','5','6','7','8','9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
FILENAME = "passwords.json"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """Generates a strong random password and copies it to the clipboard."""
    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]
    shuffle(password_list)

    password = ''.join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    messagebox.showinfo(title="Password Copied", message="Password copied to clipboard!")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    """Saves the password, website, and email to a JSON file."""
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if not website or not password:
        messagebox.showinfo(title="Validation Error", message="Please fill all required fields.")
        return
    new_data = {website: {"email": email, "password": password}}

    # Load existing data
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # Update data
    data.update(new_data)
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)

    website_entry.delete(0, END)
    password_entry.delete(0, END)
    messagebox.showinfo(title="Success", message=f"Password for {website} saved successfully!")

def search_password():
    """Searches for a website in the JSON file and displays email & password."""
    website = website_entry.get().strip()
    if not website:
        messagebox.showinfo(title="Error", message="Please enter a website to search.")
        return

    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    if website in data:
        email = data[website]["email"]
        password = data[website]["password"]
        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        pyperclip.copy(password)
    else:
        messagebox.showinfo(title="Not Found", message=f"No details found for {website}.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Logo
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0, sticky="e")
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0, sticky="e")
password_label = Label(text="Password:")
password_label.grid(row=3, column=0, sticky="e")

# Entries
website_entry = Entry(width=30)
website_entry.grid(row=1, column=1, pady=5, sticky="w")
website_entry.focus()

email_entry = Entry(width=30)
email_entry.grid(row=2, column=1, pady=5, sticky="w")
email_entry.insert(0, "aleks@gmail.com")

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, pady=5, sticky="w")

# Buttons
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(row=3, column=2, padx=5)

add_button = Button(text="Add", width=30, command=save_password)
add_button.grid(row=4, column=1, columnspan=2, pady=5)

search_button = Button(text="Search", width=10, command=search_password)
search_button.grid(row=1, column=2, padx=5)

window.mainloop()