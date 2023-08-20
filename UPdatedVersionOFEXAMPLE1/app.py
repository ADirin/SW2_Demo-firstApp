from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

# Database connection setup
db = mysql.connector.connect(
    host="127.0.0.1",
    port=3308,
    user="root",
    password="Test1234",
    database="user_db"
)
cursor = db.cursor()


@app.route('/dynamic_page')
def dynamic_page():
    # Check if user is logged in
    if 'username' in session:
        return "Welcome to the dynamic page, " + session['username']
    else:
        return "Please log in to access this page."


# ... other routes for your dynamic app ...
@app.route('/')
def home():
    # Check if user is logged in
    if 'username' in session:
        return "Welcome, " + session['username']
    else:
        return "Home Page"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Perform database query to validate user credentials
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            session['username'] = username
            return render_template('index.html')
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Perform database query to insert new user
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        return "Signup successful!"
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


@app.before_request
def require_login():
    if request.endpoint not in ['login', 'signup'] and 'username' not in session:
        return redirect('/login')


@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route("/greet", methods=["POST", "GET"])
def greet():
    flash("Hi " + str(request.form['name_input']) + ", great to see you!")
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
