import mysql.connector

from flask import Flask, render_template, request, flash, redirect, session
from flask_session import Session
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

from ling import analyze_text, read_decode_file, load_json, AnalyzedText

# configuration of the app
app = Flask(__name__)

app.config["SECRET_KEY"] = "f66ccf63243ee5f6890d462359d756fd19fc184d492dc8d124d08ff5c0e77046"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# connect app to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="lyborkiixd",
    database="linguine_test"
)

sqlcursor = db.cursor(dictionary=True, buffered=True)

def login_required(f):
    """Decorates app so some templates are accessible only when logged in."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.context_processor
def inject_user():
    """Injects logged in info into every template."""
    return dict(logged_in = True if session.get("user_id") else False)


@app.route("/", methods=["GET", "POST"])
def home():
    """The main app page – choice between analysis or exploration, and between file or text input"""
    if request.method == "POST":
        action = request.form["action"]
        language = request.form["language"]
        text_input = request.form.get("text-input")
        file_input = request.files.get("file-input")
        text_name = request.form.get("text-name")
        
        # store data in case of error, so the user doesn't have to import all data again
        session['form_data'] = request.form.to_dict()
        
        # decode .txt file, if it couldn't be decoded, redirect user to import text again
        if file_input:
            text_input = read_decode_file(file_input)
            if not text_input:
                flash("Wrong format of the text")
                return redirect("/")
        
        # check if the text was imported
        if not file_input and not text_input:
            flash("You must import a text")
            return redirect("/")            

        # if a textname was inserted, the text is saved to logged user's texts in database
        if text_name:
            sqlcursor.execute(
                "INSERT INTO texts (text, user_id, language, name) VALUES (%s, %s, %s, %s)",
                (text_input, session["user_id"], language, text_name)
            )
            db.commit()
            flash("Your text has been successfully saved to your text list!")
            return redirect("/")
        
        # create instance of the text to be processed
        text = AnalyzedText(text_input, language)

        if action == "analyze":
            text_data = analyze_text(text)
            return render_template("results_analyze.html", **text_data)
            
        elif action == "explore":
            regex_input = request.form.get("regex")
            
            # check if the regex was imported, if not, redirect user
            if len(regex_input) == 0:
                flash("You must input a word or regular expression")
                return redirect("/")
                
            sentences = text.regex_explore(regex_input)
            
            # if no sentences matching the pattern were found, redirect user
            if len(sentences) == 0:
                flash("No matching sentences found")
                return redirect("/")
            
            return render_template("results_explore.html", sentences=sentences, regex_input=regex_input)
        
    # form data to be rendered in the template, if there were any
    form_data = session.pop('form_data', {})

    return render_template("home.html", form_data=form_data)


@app.route("/mytexts", methods=["GET", "POST"])
@login_required
def profile():
    """Texts saved by the logged in user"""
    
    # render table with all texts the user has saved to their profile
    sqlcursor.execute("SELECT * FROM texts WHERE user_id = %s", (session["user_id"],))
    texts = sqlcursor.fetchall()
    
    if request.method == "POST":
        action = request.form["action"]
        text_id = request.form.get("text-name")
        delete_id = request.form.get("delete-text")
        
        # delete the text from the database
        if delete_id:
            sqlcursor.execute("DELETE FROM texts WHERE id = %s", (delete_id,))
            db.commit()
            return redirect("/mytexts")
        
        # store data in case of error, so the user doesn't have to import everything again
        session['form_data'] = request.form.to_dict()
        
        # get the user's text which was chosen to by analyzed/explored
        sqlcursor.execute("SELECT * FROM texts WHERE id = %s", (text_id,))
        db_text = sqlcursor.fetchone()
        
        # create instance of the text to be processed
        text = AnalyzedText(db_text["text"], db_text["language"])

        if action == "analyze":
            text_data = analyze_text(text)
            return render_template("results_analyze.html", **text_data)
            
        elif action == "explore":
            regex_input = request.form.get("regex")
            
            # check if the regex was imported, if not, redirect user
            if len(regex_input) == 0:
                flash("You must input a word or regular expression")
                return redirect("/mytexts")
                
            sentences = text.regex_explore(regex_input)
            
            # if no sentences matching the pattern were found, redirect user
            if len(sentences) == 0:
                flash("No matching sentences found")
                return redirect("/mytexts")
            
            return render_template("results_explore.html", sentences=sentences, regex_input=regex_input)
            
    # form data to be rendered in the template, if there were any
    form_data = session.pop('form_data', {})
    
    return render_template("mytexts.html", texts=texts, form_data=form_data)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # ensure both username and password were submitted
        if not username or not password:
            flash("Missing username or password")
            return redirect("/login")
        
        # find submitted username in database
        sqlcursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = sqlcursor.fetchone()
        if not user:
            flash("User not found")
            return redirect("/login")
        
        # check if password is correct
        correct = check_password_hash(user["password"], password)
        if not correct:
            flash("Wrong password")
            return redirect("/login")
        
        # save logged in user's ID 
        session["user_id"] = user["id"]
        
        return render_template("home.html", form_data={})
        
    return render_template("login.html")


@app.route("/bye")
def logout():
    """Log user out"""
    
    # forget session data
    session.clear()
    
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register new user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        pw_confirm = request.form.get("pw-confirm")
        
        # ensure both username and password were submitted
        if not username or not password:
            flash("You must choose both username and password")
            return redirect("/register")
        
        # ensure password matches the confirmation
        if password != pw_confirm:
            flash("Passwords don't match")
            return redirect("/register")
        
        # checks if the username doesn't already exist
        sqlcursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        found_username = sqlcursor.fetchone()
        if found_username:
            flash("Username already exists")
            return redirect("/register")
        
        else:
            # save new user and their hashed password to the database
            hashed_password = generate_password_hash(password)
            sqlcursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            db.commit()
            
            # log user in
            sqlcursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user = sqlcursor.fetchone()
            session["user_id"] = user["id"]
                        
            return render_template("home.html", form_data={})
        
    return render_template("register.html")


@app.route("/terms")
def terms():
    """Linguistic terms table – explains basic terms"""
    terms_dict = load_json("ling_terms.json", app)
    return render_template("terms.html", terms_dict=terms_dict)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)