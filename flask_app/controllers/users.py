from flask_app import app
from flask import flash, redirect, render_template, request, session
from flask_app.models.user import User
from flask_app.models.shake import Shake
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/")
def index():
    """Display the login and registration forms."""

    return render_template("index.html")


@app.post("/register")
def register_user():
    """Process the registration form."""
    # validate the form first

    # if invalid, redirect user back to form
    if not User.registration_is_valid(request.form):
        return redirect("/")
    # look for user by email on form
    potential_user = User.get_by_email(request.form["email"])
    # if there is a user, redirect to form
    if potential_user:
        flash("Email in use. Please log in.", "register")
        return redirect("/")
    print("Users not found, okay to register.")

    # hash the user's password (enctypt)
    hashed_pw = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": hashed_pw,
    }
    # save the user to the database
    user_id = User.create(data)
    # put the user's id into session
    session["user_id"] = user_id
    # message for the users when they successfully register
    flash("Thank you for registering, you're AWESOME!", "register")

    # redirect to the shake
    return redirect("/shakes")


# THIS IS FOR THE LOGIN BELOW
@app.post("/login")
def login():
    """Processes the LOGIN FORM."""
    # validate FORM first
    print("Inside the login function.")
    if not User.login_is_valid(request.form):
        print("login invalid.")
        return redirect("/")
    # check if user exists by email
    potential_user = User.get_by_email(request.form["email"])
    print(potential_user)
    # if they dont exist, flash please register and redirect
    if not potential_user:
        flash("Invalid credentials.", "login")
        print("No user.")
        return redirect("/")
    # check password if they exist
    user = potential_user
    print(user.first_name)

    # if password is wrong, flash incorrect and redirect
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid credentials.", "login")
        print("invalid password.")
        return redirect("/")

    # put the user's id into session
    session["user_id"] = user.id
    print(session["user_id"])

    # redirect to the shake
    flash("Thank you for logging in.", "login")
    return redirect("/shakes")


@app.get("/shakes")
def shakes():
    """Displays the shake template"""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    user = User.get_by_user_id(session["user_id"])
    shakes = Shake.get_all_with_users()

    return render_template("all_shakes.html", user=user, shakes=shakes)


@app.get("/logout")
def logout():
    """Clears session."""

    session.clear()
    flash("You have successfully been logged out.", "login")
    return redirect("/")
