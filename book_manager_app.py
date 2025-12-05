#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, ttk
from database_manager import DatabaseManager
from book import Book


class BookManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Manager")
        self.center_window(self.root, 800, 500)

        # DB
        self.db = DatabaseManager()
        self.db.create_table()

        # style / theme (cross-platform)
        self.style = ttk.Style()
        if "aqua" in self.style.theme_names():
            self.style.theme_use("aqua")
        elif "vista" in self.style.theme_names():
            self.style.theme_use("vista")
        else:
            self.style.theme_use("clam")

        # adapt treeview background to theme frame background
        self.style.configure("Treeview",
                             background=self.style.lookup("TFrame",
                                                          "background"),
                             fieldbackground=self.style.lookup("TFrame",
                                                               "background"))
        # selected background map (keeps cross-platform look)
        self.style.map("Treeview", background=[("selected", "#3874f2")])

        # main UI
        self._build_treeview()
        self._build_buttons()

        # initial load
        self.refresh_tree()

    # -----------------------
    # Helpers
    # -----------------------
    @staticmethod
    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    # -----------------------
    # UI builders
    # -----------------------
    def _build_treeview(self):
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(12, 6))

        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Title", "Author", "Year", "Genre"),
            show="headings",
            yscrollcommand=tree_scroll.set,
            selectmode="browse",
        )
        self.tree.pack(fill=tk.BOTH, expand=True)
        tree_scroll.config(command=self.tree.yview)

        # define columns
        self.tree.column("Title", anchor=tk.W, width=320)
        self.tree.column("Author", anchor=tk.W, width=180)
        self.tree.column("Year", anchor=tk.CENTER, width=70)
        self.tree.column("Genre", anchor=tk.W, width=140)

        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Genre", text="Genre")

    def _build_buttons(self):
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=8)

        ttk.Button(button_frame, text="ADD BOOK",
                   command=self._add_book).pack(side=tk.LEFT, padx=6)
        ttk.Button(button_frame, text="UPDATE BOOK",
                   command=self._update_book).pack(side=tk.LEFT, padx=6)
        ttk.Button(button_frame, text="DELETE BOOK",
                   command=self._delete_book).pack(side=tk.LEFT, padx=6)

    # -----------------------
    # CRUD operations
    # -----------------------
    def refresh_tree(self):
        """Reload rows from DB into the tree. Use book.id as iid (string)."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        books = self.db.get_all_books() or []
        for book in books:
            self.tree.insert("", tk.END, iid=str(book.id),
                             values=(book.title,
                                     book.author,
                                     book.year,
                                     book.genre))

    def _add_book(self):
        def SaveBook():
            title = entry_title.get().strip()
            author = entry_author.get().strip()
            year = entry_year.get().strip()
            genre = entry_genre.get().strip()

            if not title or not author or not year or not genre:
                messagebox.showwarning("Warning", "All fields are required!")
                return
            try:
                year_int = int(year)
            except ValueError:
                messagebox.showerror("Error", "Year must be a number!")
                return

            book = Book(title, author, year_int, genre)
            self.db.add_book(book)
            form.destroy()
            self.refresh_tree()

        form = tk.Toplevel(self.root)
        form.title("Add Book")
        self.center_window(form, 500, 250)
        form.resizable(False, False)

        tk.Label(form, text="Title:", anchor="e").grid(row=0,
                                                       column=0,
                                                       padx=8,
                                                       pady=6,
                                                       sticky="e")
        entry_title = tk.Entry(form, width=40)
        entry_title.grid(row=0, column=1, padx=8, pady=6, sticky="w")

        tk.Label(form, text="Author:", anchor="e").grid(row=1,
                                                        column=0,
                                                        padx=8,
                                                        pady=6,
                                                        sticky="e")
        entry_author = tk.Entry(form, width=40)
        entry_author.grid(row=1, column=1, padx=8, pady=6, sticky="w")

        tk.Label(form, text="Year:", anchor="e").grid(row=2,
                                                      column=0,
                                                      padx=8,
                                                      pady=6,
                                                      sticky="e")
        entry_year = tk.Entry(form, width=20)
        entry_year.grid(row=2, column=1, padx=8, pady=6, sticky="w")

        tk.Label(form, text="Genre:", anchor="e").grid(row=3,
                                                       column=0,
                                                       padx=8,
                                                       pady=6,
                                                       sticky="e")
        entry_genre = tk.Entry(form, width=40)
        entry_genre.grid(row=3, column=1, padx=8, pady=6, sticky="w")

        ttk.Button(form, text="SAVE", command=SaveBook).grid(row=4,
                                                             column=0,
                                                             columnspan=2,
                                                             pady=(10, 6))
        entry_title.focus_set()

    def _update_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a book first!")
            return

        book_id = int(selected[0])
        books = self.db.get_all_books() or []
        book_to_update = next((b for b in books if b.id == book_id), None)
        if not book_to_update:
            messagebox.showerror("Error", "Selected book not found in DB.")
            self.refresh_tree()
            return

        def SaveUpdate():
            title = entry_title.get().strip()
            author = entry_author.get().strip()
            year = entry_year.get().strip()
            genre = entry_genre.get().strip()

            if not title or not author or not year or not genre:
                messagebox.showwarning("Warning", "All fields are required!")
                return
            try:
                year_int = int(year)
            except ValueError:
                messagebox.showerror("Error", "Year must be a number!")
                return

            book_to_update.title = title
            book_to_update.author = author
            book_to_update.year = year_int
            book_to_update.genre = genre

            self.db.update_book(book_to_update)
            form.destroy()
            self.refresh_tree()

        form = tk.Toplevel(self.root)
        form.title("Update Book")
        self.center_window(form, 500, 250)
        form.resizable(False, False)

        tk.Label(form, text="Title:", anchor="e").grid(row=0,
                                                       column=0,
                                                       padx=8,
                                                       pady=6,
                                                       sticky="e")
        entry_title = tk.Entry(form, width=40)
        entry_title.grid(row=0, column=1, padx=8, pady=6, sticky="w")
        entry_title.insert(0, book_to_update.title)

        tk.Label(form, text="Author:", anchor="e").grid(row=1,
                                                        column=0,
                                                        padx=8,
                                                        pady=6,
                                                        sticky="e")
        entry_author = tk.Entry(form, width=40)
        entry_author.grid(row=1, column=1, padx=8, pady=6, sticky="w")
        entry_author.insert(0, book_to_update.author)

        tk.Label(form, text="Year:", anchor="e").grid(row=2,
                                                      column=0,
                                                      padx=8,
                                                      pady=6,
                                                      sticky="e")
        entry_year = tk.Entry(form, width=20)
        entry_year.grid(row=2, column=1, padx=8, pady=6, sticky="w")
        entry_year.insert(0, str(book_to_update.year))

        tk.Label(form, text="Genre:", anchor="e").grid(row=3,
                                                       column=0,
                                                       padx=8,
                                                       pady=6,
                                                       sticky="e")
        entry_genre = tk.Entry(form, width=40)
        entry_genre.grid(row=3, column=1, padx=8, pady=6, sticky="w")
        entry_genre.insert(0, book_to_update.genre)

        ttk.Button(form, text="SAVE", command=SaveUpdate).grid(row=4,
                                                               column=0,
                                                               columnspan=2,
                                                               pady=(10, 6))

    def _delete_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a book first!")
            return

        book_id = int(selected[0])
        confirm = messagebox.askyesno("Confirm", "Delete selected book?")
        if not confirm:
            return

        self.db.delete_book(book_id)
        self.refresh_tree()
        messagebox.showinfo("Deleted", "Book removed.")
