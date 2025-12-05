import tkinter as tk
from tkinter import messagebox, ttk
from database_manager import DatabaseManager
from book import Book


# -----------------------
# Helpers
# -----------------------
def center_window(window, width, height):
    """Center a Tk/Toplevel window on screen and set its size."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


# -----------------------
# Database
# -----------------------
db = DatabaseManager()
db.create_table()

# -----------------------
# Root window + ttk style (cross-platform)
# -----------------------
root = tk.Tk()
root.title("Book Manager")
center_window(root, 800, 500)

style = ttk.Style()
# prefer 'clam' theme when available for consistent styling
available_themes = style.theme_names()
if "clam" in available_themes:
    style.theme_use("clam")

# Configure button styles
style.configure("Success.TButton", foreground="white", background="#2ecc71")
style.map("Success.TButton",
          background=[("active", "#27ae60")])

style.configure("Info.TButton", foreground="white", background="#3498db")
style.map("Info.TButton",
          background=[("active", "#2980b9")])

style.configure("Danger.TButton", foreground="white", background="#e74c3c")
style.map("Danger.TButton",
          background=[("active", "#c0392b")])

style.configure("Primary.TButton", foreground="white", background="#6c5ce7")
style.map("Primary.TButton", background=[("active", "#5a4bd6")])

# -----------------------
# Treeview (table)
# -----------------------
tree_frame = ttk.Frame(root)
tree_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(12, 6))

tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical")
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(
    tree_frame,
    columns=("Title", "Author", "Year", "Genre"),
    show="headings",
    yscrollcommand=tree_scroll.set,
    selectmode="browse",
)
tree.pack(fill=tk.BOTH, expand=True)
tree_scroll.config(command=tree.yview)

# define columns
tree.column("Title", anchor=tk.W, width=320)
tree.column("Author", anchor=tk.W, width=180)
tree.column("Year", anchor=tk.CENTER, width=70)
tree.column("Genre", anchor=tk.W, width=140)

tree.heading("Title", text="Title")
tree.heading("Author", text="Author")
tree.heading("Year", text="Year")
tree.heading("Genre", text="Genre")


# -----------------------
# CRUD functions
# -----------------------
def refresh_tree():
    """Reload rows from DB into the tree. Use book.id as iid (string)."""
    # clear
    for item in tree.get_children():
        tree.delete(item)

    books = db.get_all_books() or []
    for book in books:
        # use book.id as iid so we can refer by ID later
        tree.insert("", tk.END, iid=str(book.id), values=(book.title,
                                                          book.author,
                                                          book.year,
                                                          book.genre))


def _add_book():
    """Open Add form (grid layout)"""
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
        db.add_book(book)
        form.destroy()
        refresh_tree()

    form = tk.Toplevel(root)
    form.title("Add Book")
    center_window(form, 500, 200)
    form.resizable(False, False)

    # Labels and entries using grid
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

    btn = ttk.Button(form,
                     text="SAVE",
                     style="Success.TButton",
                     command=SaveBook)
    btn.grid(row=4, column=0, columnspan=2, pady=(10, 6))

    # set focus to title
    entry_title.focus_set()


def _update_book():
    """Open Update form pre-filled with selected book values"""
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a book first!")
        return

    book_id = int(selected[0])
    books = db.get_all_books() or []
    book_to_update = next((b for b in books if b.id == book_id), None)
    if not book_to_update:
        messagebox.showerror("Error", "Selected book not found in DB.")
        refresh_tree()
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

        db.update_book(book_to_update)
        form.destroy()
        refresh_tree()

    form = tk.Toplevel(root)
    form.title("Update Book")
    center_window(form, 500, 200)
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

    ttk.Button(form, text="SAVE", style="Info.TButton",
               command=SaveUpdate).grid(row=4,
                                        column=0,
                                        columnspan=2,
                                        pady=(10, 6))


def _delete_book():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a book first!")
        return

    book_id = int(selected[0])
    confirm = messagebox.askyesno("Confirm", "Delete selected book?")
    if not confirm:
        return

    db.delete_book(book_id)
    refresh_tree()


# -----------------------
# Buttons area
# -----------------------
button_frame = ttk.Frame(root)
button_frame.pack(pady=8)

ttk.Button(button_frame,
           text="ADD BOOK",
           style="Primary.TButton",
           command=_add_book).pack(side=tk.LEFT,
                                   padx=6)
ttk.Button(button_frame,
           text="UPDATE BOOK",
           style="Info.TButton",
           command=_update_book).pack(side=tk.LEFT,
                                      padx=6)
ttk.Button(button_frame,
           text="DELETE BOOK",
           style="Danger.TButton",
           command=_delete_book).pack(side=tk.LEFT,
                                      padx=6)

# initial load
refresh_tree()

# run
root.mainloop()
