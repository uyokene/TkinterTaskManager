"""
Author: Uyoojo Okene
Date: 3/6/2025
Description: 
This is a Library Book Management System built using Tkinter in Python. 
The program allows users to:
- Login or create an account.
- Browse available books.
- Search for books by title, author, or genre.
- Borrow and return books.
- View their borrowing history.
The interface includes a background image and dynamically displays book covers.
"""

from tkinter import *
import tkinter as tk
from tkinter import messagebox
import subprocess
import os
from PIL import Image, ImageTk

# create root window
root = Tk()
# root window title and dimension
root.title("Welcome to Library Book Management System")
# Set geometry(widthxheight)
root.geometry('1000x600')
root.configure(bg="#2E7D32")  # Dark green background

# adding a label to the root window
lbl = Label(root, text="Manage your library Books with Ease")
lbl.grid()

# Load the background image
img_path = r"c:\Final project\OkeneUyoojoFinalProject\vintage library.jpg"
if os.path.exists(img_path):
    img = Image.open(img_path)
    img = img.resize((1000, 600), Image.LANCZOS)
    bg_img = ImageTk.PhotoImage(img)
    bg_label = tk.Label(root, image=bg_img)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
else:
    messagebox.showerror("Error", "Background image not found.")

# Store user credentials (Simple in-memory storage)
users = {}

# Sample book data with images (Comedy, Anime Comic, Horror, Fantasy, Image)
books = [
    {"title": "One Piece Vol.1", "author": "Eiichiro Oda", "genre": "Anime Comic", "availability": "Available",
     "image": r"c:\Final project\OkeneUyoojoFinalProject\One piece.jpg"},
    {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "genre": "Fantasy",
     "availability": "Available", "image": r"c:\Final project\OkeneUyoojoFinalProject\Harry Potter and the Sorcerers Stone.jpg"},
    {"title": "Solo Leveling Vol.1", "author": "Chugong", "genre": "Anime Comic", "availability": "Available",
     "image": r"c:\Final project\OkeneUyoojoFinalProject\Solo Leveling.jpg"},
    {"title": "Attack on Titan Vol.1", "author": "Hajime Isayama", "genre": "Anime Comic", "availability": "Available",
     "image": r"c:\Final project\OkeneUyoojoFinalProject\Attack on Titan.jpg"},
    {"title": "Death Note Vol.1", "author": "Tsugumi Ohba", "genre": "Anime Comic", "availability": "Available",
     "image": r"c:\Final project\OkeneUyoojoFinalProject\Death Note.jpg"},
    {"title": "Frankenstein", "author": "Mary Shelley", "genre": "Horror", "availability": "Available",
     "image": r"c:\Final project\OkeneUyoojoFinalProject\Frankenstein.jpg"},
    {"title": "Lord of the Rings: The Fellowship of the Ring", "author": "J.R.R. Tolkien", "genre": "Fantasy",
     "availability": "Available", "image": r"c:\Final project\OkeneUyoojoFinalProject\The Lord of the Rings.jpg"},
    {"title": "Demon Slayer Vol.1", "author": "Koyoharu Gotouge", "genre": "Anime Comic", "availability": "Available",
     "image": r"c:\Final project\OkeneUyoojoFinalProject\Demon slayer.jpg"},
    {"title": "Chainsaw Man Vol.1", "author": "Tatsuki Fujimoto", "genre": "Anime Comic", "availability": "Available",
     "image": r"c:\Final project\OkeneUyoojoFinalProject\Chainsawman.jpg"}
]

# User authentication data
users = {"user": "password"}
current_user = None
borrowed_books = {}  # {username: [book titles]}
return_history = {}  # {username: [book titles]}
user_history = {}  # {username: ["event 1", "event 2"]}

# Function to display book image
def show_book(book_title):
    for book in books:
        if book["title"] == book_title:
            book_img_path = book["image"]
            try:
                img = Image.open(book_img_path)
                img = img.resize((200, 300))
                img = ImageTk.PhotoImage(img)
                book_img_label.config(image=img)
                book_img_label.image = img
                book_title_label.config(text=book_title)
                return  # Exit function after finding the book
            except Exception as e:
                messagebox.showerror("Error", f"Image not found for {book_title}: {e}")
                return
    messagebox.showerror("Error", f"Book '{book_title}' not found.")

# Function to switch frames
def show_frame(frame):
    frame.tkraise()

# Authentication Functions
def login():
    global current_user
    username = username_entry.get()
    password = password_entry.get()
    if username in users and users[username] == password:
        current_user = username
        if username not in borrowed_books:
            borrowed_books[username] = []
        if username not in return_history:
            return_history[username] = []
        if username not in user_history:
            user_history[username] = []
        show_frame(dashboard_frame)
    else:
        messagebox.showerror("Error", "Invalid username or password")

def create_account():
    new_username = new_username_entry.get()
    new_password = new_password_entry.get()
    if new_username in users:
        messagebox.showerror("Error", "Username already exists")
    else:
        users[new_username] = new_password
        messagebox.showinfo("Success", "Account created successfully")

# Search Function
def search_books():
    search_term = search_entry.get().lower()
    search_type = search_var.get()
    results = []
    for book in books:
        if search_type == "title" and search_term in book["title"].lower():
            results.append(book["title"])
        elif search_type == "author" and search_term in book["author"].lower():
            results.append(book["title"])
        elif search_type == "genre" and search_term in book["genre"].lower():
            results.append(book["title"])
    if results:
        results_window = Toplevel(root)
        results_window.title("Search Results")
        results_text = Text(results_window, wrap="word", height=10, width=50)
        results_text.pack(padx=10, pady=10)
        for result in results:
            results_text.insert("end", result + "\n")
        results_text.config(state="disabled")
    else:
        messagebox.showinfo("Search", "No matching books found.")

def borrow_book(book_title):
    if book_title not in borrowed_books[current_user]:
        borrowed_books[current_user].append(book_title)
        user_history[current_user].append(f"Borrowed: {book_title}")
        messagebox.showinfo("Borrow", f"Thank you for borrowing {book_title}!  You have great taste in books!-- Enjoy the Adventure!")
    else:
        messagebox.showinfo("Borrow", f"You have already borrowed {book_title}.")

def return_book(book_title):
    if book_title in borrowed_books[current_user]:
        borrowed_books[current_user].remove(book_title)
        return_history[current_user].append(book_title)
        user_history[current_user].append(f"Returned: {book_title}")
        messagebox.showinfo("Return", f"Thank you for returning {book_title}! We hope it was a great read!.")
        recommend_book(book_title)
    else:
        messagebox.showinfo("Return", f"You have not borrowed {book_title}.")

def recommend_book(book_title):
    for book in books:
        if book["title"] == book_title:
            genre = book["genre"]
            recommendations = [b["title"] for b in books if b["genre"] == genre and b["title"] != book_title]
            if recommendations:
                messagebox.showinfo("Recommendation", f"You might also like: {', '.join(recommendations[:3])}")
            return

def show_history():
    history_window = Toplevel(root)
    history_window.title("User History")
    history_text = Text(history_window, wrap="word", height=10, width=50)
    history_text.pack(padx=10, pady=10)
    for event in user_history[current_user]:
        history_text.insert("end", event + "\n")
    history_text.config(state="disabled")

# Creating main frames
auth_frame = Frame(root, bg="brown")
dashboard_frame = Frame(root, bg="brown")
books_frame = Frame(root, bg="brown")
create_account_frame = Frame(root, bg="brown")
search_frame = Frame(root, bg="brown")
borrow_frame = Frame(root, bg="brown")
return_frame = Frame(root, bg="brown")
history_frame = Frame(root, bg="brown")

for frame in (auth_frame, dashboard_frame, books_frame, create_account_frame, search_frame, borrow_frame, return_frame, history_frame):
    frame.grid(row=0, column=0, sticky='news')

# Authentication Layout
Label(auth_frame, text="Login to Library", font=("Arial", 16, "bold"), bg="brown", fg="white").pack(pady=10)
Label(auth_frame, text="Username:", bg="brown", fg="white").pack()
username_entry = Entry(auth_frame)
username_entry.pack()
Label(auth_frame, text="Password:", bg="brown", fg="white").pack()
password_entry = Entry(auth_frame, show="*")
password_entry.pack()
Button(auth_frame, text="Login", command=login, width=20).pack(pady=5)
Button(auth_frame, text="Create Account", command=lambda: show_frame(create_account_frame)).pack(pady=5)

# Create Account Frame
Label(create_account_frame, text="Create Account", font=("Arial", 16, "bold"), bg="brown", fg="white").pack(pady=10)
Label(create_account_frame, text="New Username:", bg="brown", fg="white").pack()
new_username_entry = Entry(create_account_frame)
new_username_entry.pack()
Label(create_account_frame, text="New Password:", bg="brown", fg="white").pack()
new_password_entry = Entry(create_account_frame, show="*")
new_password_entry.pack()
Button(create_account_frame, text="Create", command=create_account, width=20).pack(pady=5)
Button(create_account_frame, text="Back", command=lambda: show_frame(auth_frame)).pack(pady=5)

# Dashboard Layout
Label(dashboard_frame, text="Library Dashboard", font=("Arial", 16, "bold"), bg="brown", fg="white").pack(pady=10)
Button(dashboard_frame, text="Books", command=lambda: show_frame(books_frame), width=20).pack(pady=5)
Button(dashboard_frame, text="Search Books", command=lambda: show_frame(search_frame), width=20).pack(pady=5)
Button(dashboard_frame, text="Borrow Book", command=lambda: show_frame(borrow_frame), width=20).pack(pady=5)
Button(dashboard_frame, text="Return Book", command=lambda: show_frame(return_frame), width=20).pack(pady=5)
Button(dashboard_frame, text="History", command=lambda: show_frame(history_frame), width=20).pack(pady=5)
Button(dashboard_frame, text="Exit", command=root.quit, width=20).pack(pady=5)

# Books Page Layout
Label(books_frame, text="Select a Book", font=("Arial", 14), bg="brown", fg="white").pack(pady=5)
book_list_frame = Frame(books_frame, bg="brown")
book_list_frame.pack()

for book in books:
    book_title = book["title"]
    Button(book_list_frame, text=book_title, command=lambda b=book_title: show_book(b), width=40).pack(pady=2)

book_title_label = Label(books_frame, text="", font=("Arial", 14), bg="brown", fg="white")
book_title_label.pack(pady=5)
book_img_label = Label(books_frame, bg="brown")
book_img_label.pack()
Button(books_frame, text="Back", command=lambda: show_frame(dashboard_frame), width=20).pack(pady=10)

# Search Page Layout
Label(search_frame, text="Search Books", font=("Arial", 16, "bold"), bg="brown", fg="white").pack(pady=10)
search_entry = Entry(search_frame)
search_entry.pack(pady=5)
search_var = StringVar(value="title")
Radiobutton(search_frame, text="Title", variable=search_var, value="title", bg="brown", fg="white").pack()
Radiobutton(search_frame, text="Author", variable=search_var, value="author", bg="brown", fg="white").pack()
Radiobutton(search_frame, text="Genre", variable=search_var, value="genre", bg="brown", fg="white").pack()
Button(search_frame, text="Search", command=search_books, width=20).pack(pady=5)
Button(search_frame, text="Back", command=lambda: show_frame(dashboard_frame), width=20).pack(pady=5)

# Borrow Page Layout
Label(borrow_frame, text="Borrow Book", font=("Arial", 16, "bold"), bg="brown", fg="white").pack(pady=10)
borrow_list_frame = Frame(borrow_frame, bg="brown")
borrow_list_frame.pack()
for book in books:
    book_title = book["title"]
    Button(borrow_list_frame, text=book_title, command=lambda b=book_title: borrow_book(b), width=40).pack(pady=2)
Button(borrow_frame, text="Back", command=lambda: show_frame(dashboard_frame), width=20).pack(pady=5)

# Return Page Layout
Label(return_frame, text="Return Book", font=("Arial", 16, "bold"), bg="brown", fg="white").pack(pady=10)
return_list_frame = Frame(return_frame, bg="brown")
return_list_frame.pack()
for book in books:
    book_title = book["title"]
    Button(return_list_frame, text=book_title, command=lambda b=book_title: return_book(b), width=40).pack(pady=2)
Button(return_frame, text="Back", command=lambda: show_frame(dashboard_frame), width=20).pack(pady=5)

# History Page Layout
Label(history_frame, text="User History", font=("Arial", 16, "bold"), bg="brown", fg="white").pack(pady=10)
Button(history_frame, text="Show History", command=show_history, width=20).pack(pady=5)
Button(history_frame, text="Back", command=lambda: show_frame(dashboard_frame), width=20).pack(pady=5)

show_frame(auth_frame)
root.mainloop()