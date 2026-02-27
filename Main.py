from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import json
import os

app = FastAPI(title="Book Management System (JSON Storage)")

# --- CONFIGURATION ---
DATA_FILE = "books_db.json"

# Ensure the JSON file exists so the code doesn't crash on first run
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)


# --- MODELS ---
class Book(BaseModel):
    id: str
    title: str
    author: str
    year: int


# --- DATABASE HELPERS ---
def read_db() -> List[dict]:
    """Reads the current books from the JSON file."""
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def write_db(data: List[dict]):
    """Writes the list of books back to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# --- ROUTES ---

# 1. ADD BOOK (Check if exists, then add)
@app.post("/books/", tags=["Management"])
def add_book(book: Book):
    """Checks if ID exists. If not, adds the book to the JSON file."""
    books = read_db()

    # Logic: Check if ID already exists in the list
    if any(b['id'] == book.id for b in books):
        raise HTTPException(status_code=400, detail="Book ID already exists!")

    books.append(book.dict())
    write_db(books)
    return {"message": "Book added successfully", "book": book}


# 2. SEARCH BY TITLE
@app.get("/books/search", tags=["Search & Filter"])
def search_by_title(title: str):
    """Searches for books by title (case-insensitive)."""
    books = read_db()
    # Filter list for matches
    results = [b for b in books if title.lower() in b['title'].lower()]

    if not results:
        raise HTTPException(status_code=404, detail="No books found with that title")
    return results


# 3. UPDATE BOOK
@app.put("/books/{book_id}", tags=["Management"])
def update_book(book_id: str, updated_data: Book):
    """Finds book by ID and updates its details."""
    books = read_db()
    for i, b in enumerate(books):
        if b['id'] == book_id:
            books[i] = updated_data.dict()
            write_db(books)
            return {"message": "Book updated successfully"}

    raise HTTPException(status_code=404, detail="Book not found")


# 4. DELETE BOOK
@app.delete("/books/{book_id}", tags=["Management"])
def delete_book(book_id: str):
    """Removes a book from the JSON file by ID."""
    books = read_db()
    # Keep everything EXCEPT the ID we want to delete
    new_books = [b for b in books if b['id'] != book_id]

    if len(new_books) == len(books):
        raise HTTPException(status_code=404, detail="Book not found")

    write_db(new_books)
    return {"message": "Book deleted successfully"}


# 5. LISTING ALL BOOKS
@app.get("/books/", response_model=List[Book], tags=["Listing"])
def list_all_books():
    """Returns the full list of books."""
    return read_db()


# 6. FILTERING BY AUTHOR OR YEAR
@app.get("/books/filter", tags=["Search & Filter"])
def filter_books(author: Optional[str] = None, year: Optional[int] = None):
    """Filters books based on Author, Year, or both."""
    books = read_db()
    filtered = books

    if author:
        filtered = [b for b in filtered if author.lower() in b['author'].lower()]
    if year:
        filtered = [b for b in filtered if b['year'] == year]

    return filtered


# --- SERVER STARTUP ---
if __name__ == "__main__":
    import uvicorn

    print("Server starting... Open http://127.0.0.1:8000/docs in your browser.")
    uvicorn.run(app, host="127.0.0.1", port=8000)