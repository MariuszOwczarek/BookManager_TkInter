class Book:

    def __init__(self, title: str, author: str, year: int, genre: str):
        self.id = None
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre

    def __str__(self):
        return (f'Book: {self.id}, '
                f'Title: {self.title}, '
                f'Author: {self.author}, '
                f'Year: {self.year}, '
                f'Genre: {self.genre}')

    def __repr__(self):
        return (f'Book({self.id!r}, '
                f'{self.title!r}, '
                f'{self.author!r}, '
                f'{self.year!r}, '
                f'{self.genre!r})')

