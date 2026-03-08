from fastapi import FastAPI
from routes.book_routes import router as book_router
from routes.auth_routes import router as auth_router
from routes.borrow_routes import router as borrow_router
from routes.log_routes import router as log_router
from routes.favorite_routes import router as favorite_router
from routes.rating_routes import router as rating_router
from routes.review_routes import router as review_router
from routes.reading_status_routes import router as reading_status_router
from routes.stream_routes import router as stream_router
from routes.overdue_routes import router as overdue_router
app = FastAPI(title="Book Management System")

app.include_router(auth_router)
app.include_router(book_router)
app.include_router(borrow_router)
app.include_router(log_router)
app.include_router(review_router)
app.include_router(reading_status_router)
app.include_router(favorite_router)
app.include_router(rating_router)
app.include_router(stream_router)
app.include_router(overdue_router)

