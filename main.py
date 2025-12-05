import tkinter as tk
from tkinter import messagebox, ttk
from database_manager import DatabaseManager
from book import Book


# --- BAZA DANYCH ---
db = DatabaseManager()
db.create_table()


# --- FUNKCJE ---
def refresh_list():
    """Odświeża Treeview, pokazując aktualne książki z bazy"""
    for item in tree.get_children():
        tree.delete(item)
    books = db.get_all_books() or []
    for book in books:
        tree.insert("", tk.END,
                    iid=book.id,
                    values=(book.title,
                            book.author,
                            book.year,
                            book.genre))


def _add_book():
    """Dodaje nową książkę przez formularz"""
    def SaveBook():
        title = entry_title.get()
        author = entry_author.get()
        year = entry_year.get()
        genre = entry_genre.get()

        if not title or not author or not year or not genre:
            messagebox.showwarning("Warning", "All fields are required!")
            return
        try:
            year = int(year)
        except ValueError:
            messagebox.showerror("Error", "Year must be a number!")
            return

        book = Book(title, author, year, genre)
        db.add_book(book)
        form.destroy()
        refresh_list()

    form = tk.Toplevel(root)
    form.title("Add Book")
    form.geometry("400x300")

    # Etykiety i pola obok siebie (grid)
    label_title = tk.Label(form, text="Title:")
    entry_title = tk.Entry(form)
    label_title.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_title.grid(row=0, column=1, padx=5, pady=5)

    label_author = tk.Label(form, text="Author:")
    entry_author = tk.Entry(form)
    label_author.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_author.grid(row=1, column=1, padx=5, pady=5)

    label_year = tk.Label(form, text="Year:")
    entry_year = tk.Entry(form)
    label_year.grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_year.grid(row=2, column=1, padx=5, pady=5)

    label_genre = tk.Label(form, text="Genre:")
    entry_genre = tk.Entry(form)
    label_genre.grid(row=3, column=0, padx=5, pady=5, sticky="e")
    entry_genre.grid(row=3, column=1, padx=5, pady=5)

    button_save = tk.Button(form, text="SAVE", command=SaveBook)
    button_save.grid(row=4, column=0, columnspan=2, pady=10)


def _update_book():
    """Aktualizuje zaznaczoną książkę"""
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a book first!")
        return

    book_id = int(selected[0])
    books = db.get_all_books()
    book_to_update = next((b for b in books if b.id == book_id), None)
    if not book_to_update:
        messagebox.showerror("Error", "Book not found!")
        return

    def UpdateBook():
        title = entry_title.get()
        author = entry_author.get()
        year = entry_year.get()
        genre = entry_genre.get()

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
        refresh_list()

    form = tk.Toplevel(root)
    form.title("Update Book")
    form.geometry("400x300")

    tk.Label(form, text="Title:").grid(row=0,
                                       column=0,
                                       padx=5,
                                       pady=5,
                                       sticky="e")
    entry_title = tk.Entry(form)
    entry_title.grid(row=0, column=1, padx=5, pady=5)
    entry_title.insert(0, book_to_update.title)

    tk.Label(form, text="Author:").grid(row=1,
                                        column=0,
                                        padx=5,
                                        pady=5,
                                        sticky="e")
    entry_author = tk.Entry(form)
    entry_author.grid(row=1, column=1, padx=5, pady=5)
    entry_author.insert(0, book_to_update.author)

    tk.Label(form, text="Year:").grid(row=2,
                                      column=0,
                                      padx=5,
                                      pady=5,
                                      sticky="e")
    entry_year = tk.Entry(form)
    entry_year.grid(row=2, column=1, padx=5, pady=5)
    entry_year.insert(0, str(book_to_update.year))

    tk.Label(form, text="Genre:").grid(row=3,
                                       column=0,
                                       padx=5,
                                       pady=5,
                                       sticky="e")
    entry_genre = tk.Entry(form)
    entry_genre.grid(row=3, column=1, padx=5, pady=5)
    entry_genre.insert(0, book_to_update.genre)

    tk.Button(form, text="SAVE", command=UpdateBook).grid(row=4,
                                                          column=0,
                                                          columnspan=2,
                                                          pady=10)


def _delete_book():
    """Usuwa zaznaczoną książkę"""
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a book first!")
        return

    book_id = int(selected[0])
    db.delete_book(book_id)
    refresh_list()


# --- OKNO GŁÓWNE ---
root = tk.Tk()
root.title("Book Manager")
root.geometry("600x400")

# --- Treeview z kolumnami ---
tree_frame = tk.Frame(root)
tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

tree_scroll = tk.Scrollbar(tree_frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(tree_frame,
                    yscrollcommand=tree_scroll.set,
                    selectmode="browse")

tree.pack(fill=tk.BOTH, expand=True)
tree_scroll.config(command=tree.yview)

tree["columns"] = ("Title", "Author", "Year", "Genre")
tree.column("#0", width=0, stretch=tk.NO)
tree.column("Title", anchor=tk.W, width=200)
tree.column("Author", anchor=tk.W, width=150)
tree.column("Year", anchor=tk.CENTER, width=80)
tree.column("Genre", anchor=tk.W, width=100)

tree.heading("#0", text="", anchor=tk.W)
tree.heading("Title", text="Title", anchor=tk.W)
tree.heading("Author", text="Author", anchor=tk.W)
tree.heading("Year", text="Year", anchor=tk.CENTER)
tree.heading("Genre", text="Genre", anchor=tk.W)

# --- BUTTONY ---
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame,
          text="ADD BOOK",
          command=_add_book).pack(side=tk.LEFT,
                                  padx=5)
tk.Button(button_frame,
          text="UPDATE BOOK",
          command=_update_book).pack(side=tk.LEFT,
                                     padx=5)
tk.Button(button_frame,
          text="DELETE BOOK",
          command=_delete_book).pack(side=tk.LEFT,
                                     padx=5)

refresh_list()

# --- URUCHOMIENIE OKNA ---
root.mainloop()
