from flask_app import app
from flask_app.models.like import Like
from flask import redirect, request, session


@app.post("/likes/create")
def create_like():
    """Processes the like form."""

    Like.create_like(request.form)

    return redirect("/shakes")
