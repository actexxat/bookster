import sqlite3
from flask import session, redirect
import requests
from functools import wraps
import hashlib


def remove_from_db(title):
    connection = connectDB()
    user = session['user_id']
    connection.cursor().execute('DELETE FROM books WHERE title = ? AND userid = ?', (title, user))
    connection.commit()


def update_db(title, author, year, cover, state):
    connection = connectDB()
    user = session['user_id']
    connection.cursor().execute('INSERT INTO books(title,author,year,cover,userid,shelf) VALUES(?,?,?,?,?,?)', (title, author, year, cover,user,state))
    connection.commit()
    connection.close()


def search_books(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}+intitle:{query}&maxResults=3"
    response = requests.get(url)
    data = response.json()['items']
    return data


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function


def authenticate(username, password):
    connection = connectDB()
    registered = connection.cursor().execute("SELECT username FROM users").fetchall()
    names = [item[0] for item in registered]

    password = password.encode("utf-8")
    hashValue = hashlib.sha256(password).hexdigest()

    if username in names:
        user = connection.cursor().execute("SELECT id,hash FROM users WHERE username = ?", (username,)).fetchone()
        userHash = user[1]
        userID = user[0]
        if hashValue == userHash:
            session['user_id'] = userID
            return True
        else: return False
    else: return False


def connectDB():
    connection = sqlite3.connect("bookex.db")
    return connection

def commit_close(conn):
    conn.commit()
    conn.close()