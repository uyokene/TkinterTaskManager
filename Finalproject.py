import tkinter as tk
from tkinter import messagebox

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Book Management System")
        self.root.configure(bg="#f0f0f0")  # Light background

        self.books = [
            {"title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "genre": "Sci-Fi", "available": True},
            {"title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Classic", "available": True},
            {"title": "1984", "author": "George Orwell", "genre": "Dystopian", "available": False},
            {"title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Classic", "available": True},
            {"title": "Dune", "author": "Frank Herbert", "genre": "Sci-Fi", "available": True}
        ]

        # Book Search Section
        tk.Label(root, text="Search:", bg="#f0f0f0").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.search_entry = tk.Entry(root, width=30)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(root, text="Search", command=self.search_books).grid(row=0, column=2, padx=5, pady=5)

        self.results_listbox = tk.Listbox(root, width=50, height=10)
        self.results_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        self.results_listbox.bind('<<ListboxSelect>>', self.display_book_details)

        # Book Availability Section
        tk.Label(root, text="Availability:", bg="#f0f0f0").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.availability_label = tk.Label(root, text="", bg="#f0f0f0")
        self.availability_label.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        tk.Button(root, text="Borrow", command=self.borrow_book).grid(row=3, column=0, padx=5, pady=5)
        tk.Button(root, text="Return", command=self.return_book).grid(row=3, column=1, padx=5, pady=5)

        # Book Details Section
        tk.Label(root, text="Title:", bg="#f0f0f0").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.title_label = tk.Label(root, text="", bg="#f0f0f0")
        self.title_label.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        tk.Label(root, text="Author:", bg="#f0f0f0").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.author_label = tk.Label(root, text="", bg="#f0f0f0")
        self.author_label.grid(row=5, column=1, sticky="w", padx=5, pady=5)

        tk.Label(root, text="Genre:", bg="#f0f0f0").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.genre_label = tk.Label(root, text="", bg="#f0f0f0")
        self.genre_label.grid(row=6, column=1, sticky="w", padx=5, pady=5)

    def search_books(self):
        """Searches books based on the search query."""
        query = self.search_entry.get().lower()
        self.results_listbox.delete(0, tk.END)
        results = []
        for book in self.books:
            if query in book["title"].lower() or query in book["author"].lower() or query in book["genre"].lower():
                results.append(book["title"])
        for result in results:
            self.results_listbox.insert(tk.END, result)

    def display_book_details(self, event):
        """Displays the details of the selected book."""
        selection = self.results_listbox.curselection()
        if selection:
            title = self.results_listbox.get(selection[0])
            for book in self.books:
                if book["title"] == title:
                    self.title_label.config(text=book["title"])
                    self.author_label.config(text=book["author"])
                    self.genre_label.config(text=book["genre"])
                    self.availability_label.config(text="Available" if book["available"] else "Checked Out")
                    self.selected_book = book #Store the selected book
                    return

    def borrow_book(self):
        """Borrows the selected book."""
        if hasattr(self, 'selected_book') and self.selected_book:
            if self.selected_book["available"]:
                self.selected_book["available"] = False
                self.availability_label.config(text="Checked Out")
                messagebox.showinfo("Success", f"'{self.selected_book['title']}' has been borrowed.")
            else:
                messagebox.showerror("Error", "Book is already checked out.")
        else:
            messagebox.showerror("Error", "Please select a book first.")

    def return_book(self):
        """Returns the selected book."""
        if hasattr(self, 'selected_book') and self.selected_book:
            if not self.selected_book["available"]:
                self.selected_book["available"] = True
                self.availability_label.config(text="Available")
                messagebox.showinfo("Success", f"'{self.selected_book['title']}' has been returned.")
            else:
                messagebox.showerror("Error", "Book is already available.")
        else:
            messagebox.showerror("Error", "Please select a book first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()