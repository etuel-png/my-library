from bakery import assert_equal
from final import *

def test_add_book_to_library() -> None:
    """Test that a new book is added to the reading library."""
    state = State(
        library=Library(
            username="Reader",
            fav_genre="Fantasy",
            books_read=[],
            books_to_read=[],
            read_goal=10),
        page_message="",
        current_page="Home",
        fav_books=[])
    add_book_to_library(state, "The Hobbit", "J.R.R. Tolkien",
                        "Fantasy", "5")
    assert_equal(len(state.library.books_read), 1)
    assert_equal(state.library.books_read[0].title, "The Hobbit")
    assert_equal(len(state.fav_books), 1)
test_add_book_to_library()

def test_add_book_empty() -> None:
    """Test that a book with an empty title is not added."""
    state = State(
        library=Library("Reader", "Fantasy", [], [], 10),
        page_message="",
        current_page="Home",
        fav_books=[])
    add_book_to_library(state, "", "J.R.R. Tolkien", "Fantasy", "5")
    assert_equal(len(state.library.books_read), 0)
    assert_equal(len(state.fav_books), 0)
    assert_equal(state.page_message, "Please enter a title and author.")
test_add_book_empty()

def test_save_to_read() -> None:
    """Test that a book is added to the To Read list."""
    state = State(
        library=Library("Reader", "Fantasy", [], [], 10),
        page_message="",
        current_page="Home",
        fav_books=[])
    save_to_read(state, "The Hobbit", "J.R.R. Tolkien", "Fantasy")
    assert_equal(len(state.library.books_to_read), 1)
    assert_equal(state.library.books_to_read[0].title, "The Hobbit")
    assert_equal(state.library.books_to_read[0].author, "J.R.R. Tolkien")
test_save_to_read()

def test_update_goal() -> None:
    """Test that the reading goal can be updated."""
    state = State(
        library=Library("Reader", "Fantasy", [], [], 10),
        page_message="",
        current_page="Home",
        fav_books=[])
    update_goal(state, "15")
    assert_equal(state.library.read_goal, 15)
    assert_equal(state.page_message,
                 "Your reading goal has been updated!")
test_update_goal()

def test_update_goal_invalid() -> None:
    """Test that an invalid reading goal is rejected."""
    state = State(
        library=Library("Reader", "Fantasy", [], [], 10),
        page_message="",
        current_page="Home",
        fav_books=[])
    update_goal(state, "0")
    assert_equal(state.library.read_goal, 10)
    assert_equal(state.page_message,
                 "Please enter a positive whole number.")
test_update_goal_invalid()

def test_move_book() -> None:
    """Test that a book moves from To Read to Books Read."""
    book = Book("The Hobbit", "J.R.R. Tolkien", "Fantasy", 0.0)
    state = State(
        library=Library("Reader", "Fantasy", [], [book], 10),
        page_message="",
        current_page="Home",
        fav_books=[])
    move_book(state)
    assert_equal(len(state.library.books_to_read), 0)
    assert_equal(len(state.library.books_read), 1)
    assert_equal(state.library.books_read[0].title, "The Hobbit")
test_move_book()

def test_update_genre() -> None:
    """Test that the favorite genre can be updated."""
    state = State(
        library=Library("Reader", "Fantasy", [], [], 10),
        page_message="",
        current_page="Home",
        fav_books=[])
    update_genre(state, "Mystery")
    assert_equal(state.library.fav_genre, "Mystery")
    assert_equal(state.page_message,
                 "Your favorite genre has been updated!")
test_update_genre()

def test_reading_goal() -> None:
    """Test that the reading goal page displays correctly."""
    state = State(
        library=Library("Reader", "Fantasy", [], [], 10),
        page_message="",
        current_page="Home",
        fav_books=[])
    reading_goal(state)
    assert_equal(state.current_page, "Reading Goals")
test_reading_goal()

def test_recommendations() -> None:
    """Test that the recommendations page works."""
    state = State(
        library=Library("Reader", "Mystery", [], [], 10),
        page_message="",
        current_page="Home",
        fav_books=[])
    recommendations(state)
    assert_equal(state.current_page, "Recommendations")
    assert_equal(state.library.fav_genre, "Mystery")
test_recommendations()

def test_books() -> None:
    """Test that the My Books page works."""
    book = Book("The Hobbit", "J.R.R. Tolkien", "Fantasy", 5.0)
    state = State(
        library=Library("Reader", "Fantasy", [book], [], 10),
        page_message="",
        current_page="Home",
        fav_books=[])
    books(state)
    assert_equal(state.current_page, "My Books")
    assert_equal(len(state.library.books_read), 1)
test_books()

def test_favorites() -> None:
    """Test that the Favorites page works."""
    book = Book("The Hobbit", "J.R.R. Tolkien", "Fantasy", 5.0)
    state = State(
        library=Library("Reader", "Fantasy", [], [], 10),
        page_message="",
        current_page="Home",
        fav_books=[book])
    favorites(state)
    assert_equal(state.current_page, "Favorites")
    assert_equal(len(state.fav_books), 1)
    assert_equal(state.fav_books[0].title, "The Hobbit")
test_favorites()

def test_to_read() -> None:
    """Test that the To Read page works."""
    book = Book("The Hobbit", "J.R.R. Tolkien", "Fantasy", 0.0)
    state = State(
        library=Library("Reader", "Fantasy", [], [book], 10),
        page_message="",
        current_page="Home",
        fav_books=[])
    to_read(state)
    assert_equal(state.current_page, "To Read")
    assert_equal(len(state.library.books_to_read), 1)
    assert_equal(state.library.books_to_read[0].title, "The Hobbit")
test_to_read()

def test_home() -> None:
    """Test that the home page works."""
    state = State(
        library=Library("Reader", "Fantasy", [], [], 10),
        page_message="",
        current_page="",
        fav_books=[])
    home(state)
    assert_equal(state.current_page, "Home")
    assert_equal(state.library.username, "Reader")
test_home()

def test_add_book() -> None:
    """Test that the Add a Book page works."""
    state = State(
        library=Library("Reader", "Fantasy", [], [], 10),
        page_message="",
        current_page="Home",
        fav_books=[])
    add_book(state)
    assert_equal(state.current_page, "Add a Book")
test_add_book()

def test_add_to_read() -> None:
    """Test that the Add to Read page works."""
    state = State(
        library=Library("Reader", "Fantasy", [], [], 10),
        page_message="",
        current_page="Home",
        fav_books=[])
    add_to_read(state)
    assert_equal(state.current_page, "Add to Read")
test_add_to_read()

def test_save_to_read_empty() -> None:
    """Test that an empty book is not saved."""
    state = State(
        library=Library("Reader", "Fantasy", [], [], 10),
        page_message="",
        current_page="Home",
        fav_books=[])
    save_to_read(state, "", "J.R.R. Tolkien", "Fantasy")
    assert_equal(len(state.library.books_to_read), 0)
    assert_equal(state.page_message, "Please enter a title and author.")
test_save_to_read_empty()

def test_move_book_empty() -> None:
    """Test moving a book when the To Read list is empty."""
    state = State(
        library=Library("Reader", "Fantasy", [], [], 10),
        page_message="",
        current_page="Home",
        fav_books=[])
    move_book(state)
    assert_equal(len(state.library.books_read), 0)
    assert_equal(state.page_message, "Your To Read list is empty.")
test_move_book_empty()