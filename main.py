from flask import Flask,flash, request, render_template, g, session, redirect, jsonify,url_for
from flask_session import Session
from helpers import update_db, removeFromDB, search_books, login_required, authenticate
import hashlib
import sqlite3


app = Flask(__name__)
app.secret_key = "MYSUPERSEKRETCOOCKIEKEyyyyY"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route("/", methods=['POST', "GET"])
def login():
    if request.method == "POST":
        userName = request.form.get("username")
        password = request.form.get("password")
        if (authenticate(userName, password)):
            return redirect(url_for('home'))
        else: flash("User Does Not Exist or Wrong Password")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        userName = request.form.get("username")
        password = request.form.get("password")
        passwordConfirmation = request.form.get("password-con")
        email = request.form.get("email")
        
        if password == passwordConfirmation:
            connection = sqlite3.connect("bookex.db")
            occupied = connection.cursor().execute("SELECT username FROM users")
            for name in occupied:
                if userName == name[0]:
                    return "Username Taken."

            if len(userName) < 4:
                return "USERNAME length too small"
            if len(password) < 8:
                return "Password Length Too Small"
            if password != passwordConfirmation:
                return "Passwords do not Match"
            password = password.encode('utf-8')  # Convert the password to bytes
            hash_object = hashlib.sha256(password)  # Choose a hashing algorithm (e.g., SHA-256)
            hex_dig = hash_object.hexdigest()  # Get the hexadecimal digest of the hashed password

            connection.cursor().execute("INSERT INTO users(username, hash, email) VALUES(?, ?, ?)", (userName, hex_dig, email))
            connection.commit()
            connection.close()
            flash("Registration Successful!")
            return render_template("login.html")
    return render_template("register.html")


@app.route("/home",methods=['POST', 'GET'])
@login_required
def home():
    user = session['user_id']
    connection = sqlite3.connect("bookex.db")
    db_books = connection.cursor().execute("SELECT bookid,cover,title,author,year,username,shelf FROM books INNER JOIN users ON books.userid = users.id WHERE userid = ?",(user,))

    return render_template("home.html", data=list(db_books))

@app.route("/results", methods=['POST'])
@login_required
def show_search():
    if request.method == "POST":
        title = request.form.get("search")
        books = search_books(title)
        results = []
        for book in books:
            item = {
                "title":book["volumeInfo"]['title'],
                "author":book["volumeInfo"]['authors'],
            }
            if 'imageLinks' in book['volumeInfo']:
                item['cover'] = book['volumeInfo']['imageLinks']['thumbnail']
            if 'publishedDate' in book['volumeInfo']:
                item['year']  = book['volumeInfo']['publishedDate']
            results.append(item)
        return render_template("results.html", data=results)


@app.route("/get", methods=['POST'])
@login_required
def get_data():
    if request.method == 'POST':
        data = request.get_json()
        title = data['title']
        author = data['author']
        cover = data['cover']
        state = data['state']
        if data['year']:
            year = data['year']
        else:
            year = 'N/A'

        update_db(title, author, year, cover,state)
        return redirect(url_for('home'))



@app.route("/remove", methods=['POST'])
@login_required
def get_remove():
    if request.method == 'POST':
        data = request.get_json()
        title = data['title']
        removeFromDB(title)
    return redirect(url_for('home'))

