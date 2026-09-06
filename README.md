# 🎬 Top Movies Web Application

A simple **Top Movies web application** built with **Flask, Flask-SQLAlchemy, SQLite, Bootstrap 5, Flask-WTF, Jinja2, and The Movie Database (TMDB) API**.

This project was created as a learning project to practice Flask, SQLAlchemy, SQLite, APIs, forms, Jinja2, and CRUD operations.

## 🚀 Features

- 🔎 Search for movies using the TMDB API
- 🎬 Display movie search results
- ➕ Add a selected movie to the local SQLite database
- ⭐ Give a movie a rating
- 📝 Add a personal review
- 🏆 Automatically calculate movie rankings based on rating
- ✏️ Update movie rating and review
- 🗑️ Delete movies
- 📱 Bootstrap-based interface
- 🔐 Store the TMDB API key in a `.env` file
- 🔄 Retry the API request up to 10 times if a request error occurs

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Web application/backend |
| Flask-SQLAlchemy | Database and ORM |
| SQLAlchemy | Working with database tables and records |
| SQLite | Local database |
| Flask-WTF | Forms and form validation |
| Bootstrap 5 | UI styling |
| Jinja2 | Dynamic HTML templates |
| Requests | Calling the TMDB API |
| python-dotenv | Loading environment variables |
| TMDB API | Searching for movies |

## 📁 Project Structure

```text
project/
│
├── instance/
│   └── new-books-collection.db
│
├── static/
│   └── css/
│       └── styles.css
│
├── templates/
│   ├── add.html
│   ├── base.html
│   ├── edit.html
│   ├── index.html
│   └── select.html
│
├── .env
├── .gitignore
├── main.py
└── README.md
```

> The SQLite database is created inside Flask's `instance` folder because the application uses a relative SQLite database URI.

## ⚙️ Installation

### 1. Clone the project

```bash
git clone <your-github-repository-url>
cd <project-folder>
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install flask flask-bootstrap5 flask-sqlalchemy flask-wtf requests python-dotenv
```

If you have a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file in the same folder as `main.py`.

The current code reads the variable named `api_key`:

```env
api_key=YOUR_TMDB_API_KEY
```

The code loads it with:

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("api_key")
```

### Important

Do **not** upload your real `.env` file to GitHub.

Add this to `.gitignore`:

```text
.env
```

## 🗄️ Database

The project uses SQLite with Flask-SQLAlchemy:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
```

The `Movie` model represents the `movie` table:

```python
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    year: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String, nullable=True)
    img_url: Mapped[str] = mapped_column(String, nullable=False)
```

The table is created with:

```python
with app.app_context():
    db.create_all()
```

## 🔄 How the Application Works

### 1. Home Page

The `/` route gets all movies from the database and orders them by rating.

```python
db.select(Movie).order_by(Movie.rating)
```

The list is then reversed so the highest-rated movie appears first.

The ranking is calculated using:

```python
all_cards[a].ranking = len(all_cards) - a
```

### 2. Add Movie

The `/add` route displays a form where the user enters a movie name.

The application sends the movie name to TMDB:

```python
requests.get(
    url,
    params={
        "api_key": api_key,
        "query": Movie_name
    }
)
```

The search results are then displayed on `select.html`.

### 3. Select Movie

The `/select/<int:id>` route receives the TMDB movie ID.

The selected movie's information is saved into the local database:

```python
new_movie = Movie(
    title=user['original_title'],
    year=user['release_date'],
    description=user['overview'],
    img_url=f"https://image.tmdb.org/t/p/w500{user['poster_path']}"
)
```

After saving, the user is redirected to the update page so they can add a rating and review.

### 4. Update Movie

The `/update/<int:id>` route allows the user to update:

- Rating
- Review

```python
edit_data.review = user_review
edit_data.rating = user_rating

db.session.commit()
```

### 5. Delete Movie

The `/delete/<int:id>` route finds a movie by its ID and deletes it:

```python
db.session.delete(d_data)
db.session.commit()
```

## 🔁 API Retry Logic

The movie search currently tries the API request up to 10 times:

```python
for i in range(10):
    try:
        api_data = requests.get(
            url,
            params={
                "api_key": api_key,
                "query": Movie_name
            }
        )

        supers = api_data.json()["results"]

        return render_template(
            "select.html",
            data_user=supers
        )

    except requests.exceptions.RequestException:
        pass
```

If the request succeeds, `return` immediately stops the loop.

If a `RequestException` occurs, the next attempt starts.

## ▶️ Run the Application

Run:

```bash
python main.py
```

Then open:

```text
http://127.0.0.1:5000/
```

## 📌 Main Routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Show all saved movies |
| `/add` | GET, POST | Search for a movie using TMDB |
| `/select/<id>` | GET | Save the selected movie |
| `/update/<id>` | GET, POST | Update rating and review |
| `/delete/<id>` | GET | Delete a movie |

## 🧠 What I Learned From This Project

This project helped practice the complete flow:

```text
HTML Form
    ↓
Flask Route
    ↓
TMDB API
    ↓
Jinja2 Template
    ↓
Select Movie
    ↓
SQLAlchemy
    ↓
SQLite Database
    ↓
Update / Delete
    ↓
Display Movies
```

## ⚠️ Notes

### Duplicate Movie Titles

The `title` column uses:

```python
unique=True
```

Therefore, the same movie title cannot be inserted into the database twice.

If you try to add the same title again, SQLite raises a `UNIQUE constraint failed` error.

### Rating Can Be Empty

The current model uses:

```python
rating = mapped_column(Float, nullable=True)
```

Therefore, a newly added movie can initially have no rating. The rating can be added later from the update page.
