from dataclasses import dataclass
from drafter import *
set_website_title("My Library")
set_site_information(
    author="Lizzie Tuel",
    description="Track your reading and get new recommendations.",
    sources="Thanks to the Drafter docs and my LLM.",
    planning = "",
    links=[])
hide_debug_information()
set_website_framed(False)

@dataclass
class Book:
    title: str
    author: str
    genre: str
    rating: float
@dataclass
class Library:
    username: str
    fav_genre: str
    books_read: list[Book]
    books_to_read: list[Book]
    read_goal: int
@dataclass
class State:
    library: Library
    page_message: str
    current_page: str
    fav_books: list[Book]

initial_state = State(
    library=Library(username="Reader", fav_genre="Fantasy", books_read=[],
        books_to_read=[], read_goal=10),
    page_message="Welcome to your reading tracker!",
    current_page="Home",
    fav_books=[])


@route("/")
def home(state: State) -> Page:
    """Display the welcome page of the reading tracker."""
    state.current_page = "Home"
    return Page(state, [Header("My Reading Tracker"),
        "Welcome to your personal reading tracker!",
        "Hello, " + state.library.username + "!",
        "Keep track of your books and discover new ones.",
        Button("My Books", "/books"),
        Button("Add a Book", "/add-book"),
        Button("Recommendations", "/recommendations"),
        Button("Reading Goals", "/reading-goal"),
        Button("Favorites", "/favorites"),
        Button("To Read List", "/to-read")])

@route("/books")
def books(state: State) -> Page:
    """Display all books in the user's library."""
    state.current_page = "My Books"
    book_list = []
    for book in state.library.books_read:
        book_list.append(book.title + " by " + book.author + " - Rating: " + str(book.rating))
    if len(state.library.books_read) == 0:
        book_list.append("You haven't added any books yet!")
    return Page(state, [Header("My Books"),
        "Here are the books you have read:", *book_list, Button("Home", "/")])

@route("/add-book")
def add_book(state: State) -> Page:
    """Display the form for adding a new book."""
    state.current_page = "Add a Book"
    return Page(state, [Header("Add a New Book"),
        TextBox("title", "Book Title"),
        TextBox("author", "Author"),
        SelectBox("genre", ["Fantasy", "Mystery", "Romance",
                            "Fiction", "Science Fiction","Nonfiction"]),
        SelectBox("rating", ["1","2","3","4","5"]),
        Button("Add Book", "/add-book-to-library"),
        Button("Home", "/")])

@route("/add-book-to-library")
def add_book_to_library(state: State, title: str,
                        author: str, genre: str, rating: str) -> Page:
    """Save a new book to the user's reading library."""
    if title == "" or author == "":
        state.page_message = "Please enter a title and author."
    else:
        book_rating = float(rating)
        new_book = Book(title, author, genre, book_rating)
        state.library.books_read.append(new_book)
        if book_rating == 5:
            state.fav_books.append(new_book)
        state.page_message = "Book successfully added!"
    return Page(state, [Header("Add Book"),
        state.page_message,
        Button("Add Another Book", "/add-book"),
        Button("View My Books", "/books"),
        Button("Home", "/")])

@route("/favorites")
def favorites(state: State) -> Page:
    """Display all of the user's favorite books."""
    state.current_page = "Favorites"
    favorite_list = []
    for book in state.fav_books:
        favorite_list.append(book.title + " by " + book.author)
    if len(state.fav_books) == 0:
        favorite_list.append("You haven't added any favorite books yet!")
    return Page(state, [Header("My Favorite Books"),
        "Here are your favorite books:", *favorite_list,
        Button("Home", "/"),Button("My Books", "/books")])

@route("/recommendations")
def recommendations(state: State) -> Page:
    """Recommend books based on the user's favorite genre."""
    state.current_page = "Recommendations"
    if state.library.fav_genre == "Fantasy":
        recommended_books = [Book("The Hobbit", "J.R.R. Tolkien", "Fantasy", 5),
            Book("The Lightning Thief", "Rick Riordan", "Fantasy", 5)]
    elif state.library.fav_genre == "Mystery":
        recommended_books = [Book("The Westing Game", "Ellen Raskin", "Mystery", 5),
            Book("Nancy Drew", "Carolyn Keene", "Mystery", 5)]
    elif state.library.fav_genre == "Romance":
        recommended_books = [Book("Pride and Prejudice", "Jane Austen", "Romance", 5),
            Book("Emma", "Jane Austen", "Romance", 5)]
    elif state.library.fav_genre == "Science Fiction":
        recommended_books = [Book("Dune", "Frank Herbert", "Science Fiction", 5),
            Book("Ender's Game", "Orson Scott Card", "Science Fiction", 5)]
    elif state.library.fav_genre == "Nonfiction":
        recommended_books = [Book("Hidden Figures", "Margot Lee Shetterly", "Nonfiction", 5),
        Book("The Diary of a Young Girl", "Anne Frank", "Nonfiction", 5)]
    else:
        recommended_books = [Book("The Giver", "Lois Lowry", "Fiction", 5),
            Book("Wonder", "R.J. Palacio", "Fiction", 5)]
    recommendation_list = []
    for book in recommended_books:
        recommendation_list.append(book.title + " by " + book.author)
    return Page(state, [Header("Book Recommendations"),"Here are some books you might enjoy:",
        *recommendation_list,
        Button("Home", "/"),
        Button("My Books", "/books"),
        SelectBox("new_genre", ["Fantasy","Mystery","Romance","Fiction",
                "Science Fiction","Nonfiction"]),
        Button("Update Favorite Genre", "/update-genre")])

@route("/update-genre")
def update_genre(state: State, new_genre: str) -> Page:
    """Update the user's favorite genre."""
    state.library.fav_genre = new_genre
    state.page_message = "Your favorite genre has been updated!"
    return Page(state, [Header("Favorite Genre"),
        state.page_message,
        Button("View Recommendations", "/recommendations"),
        Button("Home", "/")])

@route("/reading-goal")
def reading_goal(state: State) -> Page:
    """Display the user's reading goal and progress."""
    state.current_page = "Reading Goals"
    books_finished = len(state.library.books_read)
    if books_finished >= state.library.read_goal:
        goal_message = "Congratulations! You reached your reading goal!"
    else:
        books_left = state.library.read_goal - books_finished
        goal_message = "You have " + str(books_left) + " books left to reach your goal."
    return Page(state, [Header("My Reading Goals"),
        "Your reading goal is " + str(state.library.read_goal) + " books.",
        "You have read " + str(books_finished) + " books.", goal_message,
        Button("Home", "/"),
        Button("My Books", "/books"),
        TextBox("new_goal", "Enter your new reading goal"),
        Button("Update Goal", "/update-goal")])

@route("/update-goal")
def update_goal(state: State, new_goal: str) -> Page:
    """Update the user's reading goal."""
    if new_goal.isdigit() and int(new_goal) > 0:
        state.library.read_goal = int(new_goal)
        state.page_message = "Your reading goal has been updated!"
    else:
        state.page_message = "Please enter a positive whole number."
    return Page(state,[Header("Reading Goal"),
        state.page_message,
        Button("View Reading Goals", "/reading-goal"),
        Button("Home", "/")])

@route("/to-read")
def to_read(state: State) -> Page:
    """Display books the user wants to read."""
    state.current_page = "To Read"
    to_read_list = []
    for book in state.library.books_to_read:
        to_read_list.append(book.title + " by " + book.author)
    if len(state.library.books_to_read) == 0:
        to_read_list.append("Your To Read list is empty!")
    return Page(state, [Header("My To Read List"),"Here are the books you want to read:",
        *to_read_list, Button("Home", "/"), Button("My Books", "/books"), Button("Add a Book", "/add-to-read"),
        Button("Move First Book to Books Read", "/move-book")])

@route("/add-to-read")
def add_to_read(state: State) -> Page:
    """Display a form for adding books to the To Read list."""
    state.current_page = "Add to Read"
    return Page(state, [Header("Add a Book to Your To Read List"),
        TextBox("title", "Book Title"),
        TextBox("author", "Author"),
        SelectBox("genre", ["Fantasy", "Mystery", "Romance",
        "Fiction", "Science Fiction", "Nonfiction"]),
        Button("Save Book", "/save-to-read"),
        Button("Home", "/")])

@route("/save-to-read")
def save_to_read(state: State, title: str, author: str, genre: str) -> Page:
    """Save a book to the user's To Read list."""
    if title == "" or author == "":
        state.page_message = "Please enter a title and author."
    else:
        new_book = Book(title, author, genre, 0.0)
        state.library.books_to_read.append(new_book)
        state.page_message = "Book added to your To Read list!"
    return Page(state,[Header("To Read List"),
        state.page_message,
        Button("View To Read List", "/to-read"),
        Button("Add Another Book", "/add-to-read"),
        Button("Home", "/")])

@route("/move-book")
def move_book(state: State) -> Page:
    """Move a book from To Read to Books Read."""
    if len(state.library.books_to_read) > 0:
        finished_book = state.library.books_to_read.pop(0)
        state.library.books_read.append(finished_book)
        state.page_message = "Book moved to Books Read!"
    else:
        state.page_message = "Your To Read list is empty."
    return Page(state,[Header("Move a Book"),
        state.page_message,
        Button("View My Books", "/books"),
        Button("View To Read List", "/to-read"),
        Button("Home", "/")])

if __name__ == "__main__":
    start_server(initial_state)
