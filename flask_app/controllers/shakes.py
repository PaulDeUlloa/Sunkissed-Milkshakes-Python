import datetime
from flask_app import app
from flask import flash, redirect, render_template, request, session
from flask_app.models.user import User
from flask_app.models.shake import Shake


@app.template_filter("format_date")
def format_date(date):
    return date.strftime("%Y-%m-%d")


@app.route("/shakes")
def all_shakes():
    """Display the all_shakes template."""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    user = User.get_by_user_id(session["user_id"])
    shakes = Shake.get_all_with_users()

    return render_template("all_shakes.html", user=user, shakes=shakes)


@app.get("/shakes/new")
def new_shake():
    """Displays the new shake template"""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    user = User.get_by_user_id(session["user_id"])
    return render_template("new_shake.html", user=user)


@app.post("/shakes/create")
def create_shake():
    """Processes the new shake table form"""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    if not Shake.form_is_valid(request.form):
        return redirect("/shakes/new")

    Shake.create(request.form)
    return redirect("/shakes")


@app.get("/shakes/<int:shake_id>")
def shake_details(shake_id):
    """Displays the shake_details.html template."""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    user = User.get_by_user_id(session["user_id"])
    shake = Shake.get_one_with_user(shake_id)
    # count = Like.get_like_count(shake_id)

    return render_template("shake_details.html", user=user, shake=shake)


# count=count


@app.get("/shakes/<int:shake_id>/edit")
def edit_shake(shake_id):
    """Displays the edit_shake.html template."""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    user = User.get_by_user_id(session["user_id"])
    shake = Shake.get_one_with_user(shake_id)

    return render_template("edit_shake.html", user=user, shake=shake)


@app.post("/shakes/<int:shake_id>/update")
def update_shake(shake_id):
    """Process the edit shake form."""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    Shake.update_shake(request.form)
    return redirect(f"/shakes/{shake_id}")


@app.post("/shake/<int:shake_id>/delete")
def delete_shake(shake_id):
    """Deletes a shake by it's id."""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")
    Shake.delete_shake(shake_id)

    return redirect("/shakes")
