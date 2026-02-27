# Redis_project
# 📚 Book Management System (FastAPI + JSON)

A lightweight REST API built with **Python** and **FastAPI** to manage a book collection. This project uses a local **JSON file** for data persistence, meaning it requires zero external database setup.

## 🚀 Key Features
* **Add Books**: Prevent duplicates with automatic ID existence checks.
* **Search**: Find books by title (case-insensitive).
* **Filter**: Narrow down results by **Author** or **Year of Publication**.
* **Full CRUD**: Support for viewing, updating, and deleting records.
* **Auto-Docs**: Interactive Swagger UI for instant testing.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
    cd YOUR_REPO_NAME
    ```

2.  **Create a Virtual Environment (Optional but Recommended):**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install fastapi uvicorn
    ```

## 🏃 Running the Application
Start the server using the following command:
```bash
python Main.py
