import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, flash
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from helpers import login_required, apology 

# Configure application
app = Flask(__name__)

upload_folder = "static/photos/"
app.config["UPLOAD_FOLDER"] = upload_folder

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///fashion.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#sends the user to homepage
@app.route("/")
@login_required
def index():
    return render_template("index.html")

#sends the user to mycloset page as well as creates a list of clothing items in a specific user's closet
@app.route("/mycloset", methods=["GET", "POST"])
@login_required
def mycloset():
    closet = db.execute("SELECT * FROM clothing WHERE userid = ?", session["user_id"])
    return render_template("mycloset.html", closet=closet)

#creates lists of all clothing items pertaining to a specific type
@app.route("/typesort", methods=["GET", "POST"])
@login_required
def typesort():
    #create a list of clothing for each type 
    hats = db.execute("SELECT * FROM clothing WHERE type = ?", "hat")
    shirts = db.execute("SELECT * FROM clothing WHERE type = ?", "shirt")
    jackets = db.execute("SELECT * FROM clothing WHERE type = ?", "jacket")
    dresses = db.execute("SELECT * FROM clothing WHERE type =?","dress")
    pantss = db.execute("SELECT * FROM clothing WHERE type = ?", "pants")
    shoess = db.execute("SELECT * FROM clothing WHERE type = ?", "shoes")
    return render_template("typesort.html", hats=hats, shirts = shirts, jackets = jackets, dresses = dresses, pantss = pantss, shoess = shoess)

#creates lists of all clothing items pertaining to a specific color category 
@app.route("/colorsort", methods=["GET", "POST"])
@login_required
def colorsort():
    #create a list for each color option 
    reds = db.execute("SELECT * FROM clothing WHERE color = ?", "red")
    blues = db.execute("SELECT * FROM clothing WHERE color = ?", "blue")
    greens = db.execute("SELECT * FROM clothing WHERE color = ?", "green")
    yellows = db.execute("SELECT * FROM clothing WHERE color = ?", "yellow")
    oranges = db.execute("SELECT * FROM clothing WHERE color = ?", "orange")
    blacks = db.execute("SELECT * FROM clothing WHERE color = ?", "black")
    whites = db.execute("SELECT * FROM clothing WHERE color = ?", "white")
    pinks = db.execute("SELECT * FROM clothing WHERE color = ?", "pink")
    navys = db.execute("SELECT * FROM clothing WHERE color = ?", "navy")
    greys = db.execute("SELECT * FROM clothing WHERE color = ?", "grey")
    browns = db.execute("SELECT * FROM clothing WHERE color = ?", "brown")
    purples = db.execute("SELECT * FROM clothing WHERE color = ?", "purple")
    return render_template("colorsort.html", reds = reds, blues = blues, greens = greens, yellows = yellows, oranges = oranges, blacks = blacks, whites = whites, purples = purples, pinks = pinks, navys = navys, greys = greys, browns = browns)

#ensures the user inputted required criteria and inserts observation into the database
@app.route("/addnew", methods=["GET", "POST"])
@login_required
def addnew():
        # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("name"):
            return apology("must provide name", 403)
        #ensures the user submitted a type
        elif not request.form.get("type"): 
            return apology("must provide type", 403)
        #ensures the user submitted a color option
        elif not request.form.get("color"):
            return apology("must provide color", 403)
        #uploads image to photo folder and creates a variable that references the photo
        photo = request.files["image"]
        getname = photo.filename
        photo.save(os.path.join(
            app.config['UPLOAD_FOLDER'], secure_filename(photo.filename)
        ))
        #inserts observation into clothing table 
        db.execute("INSERT INTO clothing(userid, name, type, color, photo) VALUES (?, ?, ?, ?, ?)", session["user_id"], request.form.get("name"), request.form.get("type"), request.form.get("color"), getname)
        # Redirect user to closet page
        return redirect("/mycloset")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("addnew.html")

#creates a list of all outfits that users submitted into the explore page
@app.route("/explore", methods=["GET", "POST"])
@login_required
def explore():
    explore = db.execute("SELECT * FROM outfits")
    return render_template("explore.html", explore=explore)

#ensures the user inputted required criteria and inserts observation into the database
@app.route("/addnewoutfit", methods=["GET", "POST"])
@login_required
def addnewoutfit():
        # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("name"):
            return apology("must provide name", 403)
        #uploads photo into photos folder and creates a reference for that photo
        photo = request.files["image"]
        getname = photo.filename
        photo.save(os.path.join(
            app.config['UPLOAD_FOLDER'], secure_filename(photo.filename)
        ))
        #inserts observation into the outfits table
        db.execute("INSERT INTO outfits(userid, name, photo) VALUES (?, ?, ?)", session["user_id"], request.form.get("name"), getname)
        # Redirect user to explore
        return redirect("/explore")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("addnewoutfit.html")

#deletes the clothing item that the user wants to delete from their closet
@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    if request.method == "POST":
        #deletes selected item from clothing table
        db.execute("DELETE FROM clothing WHERE itemid = ?", request.form.get("idnumber"))
        return redirect("/mycloset")
    else:
        #redirects user to mycloset page
        return redirect("/mycloset")

#same thing as delete function except sends the user back to the colorsort page
@app.route("/colordelete", methods=["GET", "POST"])
@login_required
def colordelete():
    if request.method == "POST":
        db.execute("DELETE FROM clothing WHERE itemid = ?", request.form.get("idnumber"))
        return redirect("/colorsort")
    else:
        return redirect("/colorsort")

#same thing as the delete function but sends the user back to the typesort page
@app.route("/typedelete", methods=["GET", "POST"])
@login_required
def typedelete():
    if request.method == "POST":
        db.execute("DELETE FROM clothing WHERE itemid = ?", request.form.get("idnumber"))
        return redirect("/typesort")
    else:
        return redirect("/typesort")
    
#allows the user to log into their account 
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["userid"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

#allows the user to logout from their account
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

#creates lists of size 1 with random article of clothing for each type of clothing 
@app.route("/randomize")
@login_required
def randomize():
    hat = db.execute("SELECT photo, name, color FROM clothing WHERE type = 'hat' ORDER BY RANDOM() LIMIT 1")
    shirt = db.execute("SELECT photo, name, color FROM clothing WHERE type = 'shirt' ORDER BY RANDOM() LIMIT 1")
    pants = db.execute("SELECT photo, name, color FROM clothing WHERE type = 'pants' ORDER BY RANDOM() LIMIT 1")
    shoes = db.execute("SELECT photo, name, color FROM clothing WHERE type = 'shoes' ORDER BY RANDOM() LIMIT 1")
    jacket = db.execute("SELECT photo, name, color FROM clothing WHERE type = 'jacket' ORDER BY RANDOM() LIMIT 1")
    return render_template("randomize.html", hat=hat, shirt = shirt, pants = pants, shoes = shoes, jacket = jacket)

#directs user to outfits page
@app.route("/outfits")
@login_required
def outfits():
    return render_template("outfits.html")

#allows the user to register an account onto the website
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
        # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        #ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 403)

        #ensure username not taken
        if len(db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))) >= 1:
            return apology("Username already taken", 403)

        #check if confirmation matches password
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match.")

        #add new user
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))
        #Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["userid"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)