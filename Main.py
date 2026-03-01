from fastapi import FastAPI
from routes.book_routes import router as book_router
from routes.favorite_routes import router as favorite_router
from routes.reading_list_routes import router as reading_list_router
from routes.borrow_routes import router as borrow_router
from routes.log_routes import router as log_router

app = FastAPI(title="Book Management System")

app.include_router(book_router)
app.include_router(favorite_router)
app.include_router(reading_list_router)
app.include_router(borrow_router)
app.include_router(log_router)

if __name__ == "__main__":
    import uvicorn
    print("Server starting... Open http://127.0.0.1:8000/docs in your browser.")
    uvicorn.run(app, host="127.0.0.1", port=8000)