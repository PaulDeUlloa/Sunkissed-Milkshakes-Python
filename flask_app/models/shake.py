from flask import flash
from flask_app.models.user import User
from flask_app.models.like import Like
from flask_app.config.mysqlconnection import connectToMySQL


DATABASE = "python_project"


class Shake:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.difficulty = data["difficulty"]
        self.is_under_5 = data["is_under_5"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.user = None
        # if you are required to display on the page who created that gizmo or uploaded that gizmo to the website you would switch NONE with

    @staticmethod
    def form_is_valid(form_data):
        """Validates the create shake form."""

        is_valid = True
        # NAME VALIDATION
        if len(form_data["name"].strip()) == 0:
            is_valid = False
            flash("Please enter name.", "name")
        elif len(form_data["name"].strip()) < 3:
            is_valid = False
            flash("Name must be at least three characters.", "name")
        # DESCRIPTION VALIDATION
        if len(form_data["description"].strip()) == 0:
            is_valid = False
            flash("Please enter description.", "name")
        elif len(form_data["description"].strip()) < 3:
            is_valid = False
            flash("Description must be at least three characters.", "name")
        # INSTRUCTIONS VALIDATION
        if len(form_data["instructions"].strip()) == 0:
            is_valid = False
            flash("Please enter instructions.", "name")
        elif len(form_data["instructions"].strip()) < 3:
            is_valid = False
            flash("Instructions must be at least three characters.", "name")
        if len(form_data["instructions"].strip()) > 600:
            is_valid = False
            flash("Instructions must be at less than 360 characters.", "name")
        # DIFFICULTY VALIDATION
        if len(form_data["difficulty"].strip()) == 0:
            is_valid = False
            flash("Please enter difficulty.", "name")
        #! Should work if I update the new_shake.html difficulty input type
        # elif int(form_data["difficulty"].strip()) < 5:
        #     is_valid = False
        #     flash("Difficulty must be between 1-5 values.", "name")
        # UNDER 5 MIN VALIDATION
        if "is_under_5" not in form_data:
            is_valid = False
            flash("Please enter if shake can be made under 5 minutes.", "name")

        return is_valid

    @staticmethod
    def edit_form_is_valid(form_data):
        """Validates the edit shake form."""

        is_valid = True
        # NAME VALIDATION
        if len(form_data["name"].strip()) == 0:
            is_valid = False
            flash("Please enter name.", "edit")
        elif len(form_data["name"].strip()) < 3:
            is_valid = False
            flash("Name must be at least three characters.", "edit")
        # DESCRIPTION VALIDATION
        if len(form_data["description"].strip()) == 0:
            is_valid = False
            flash("Please enter description.", "edit")
        elif len(form_data["description"].strip()) < 3:
            is_valid = False
            flash("Description must be at least three characters.", "edit")
        # INSTRUCTIONS VALIDATION
        if len(form_data["instructions"].strip()) == 0:
            is_valid = False
            flash("Please enter instructions.", "edit")
        elif len(form_data["instructions"].strip()) < 3:
            is_valid = False
            flash("Instructions must be at least three characters.", "edit")
        if len(form_data["instructions"].strip()) > 600:
            is_valid = False
            flash("Instructions must be at less than 360 characters.", "edit")
        # DIFFICULTY VALIDATION
        if len(form_data["difficulty"].strip()) == 0:
            is_valid = False
            flash("Please enter difficulty.", "edit")
        # elif len(form_data["difficulty"].strip()) != [1, 2, 3, 4, 5]:
        #     is_valid = False
        #     flash("Difficulty must be between 1-5 values.", "edit")
        # UNDER 5 MIN VALIDATION
        if "is_under_5" not in form_data:
            is_valid = False
            flash("Please enter if shake can be made under 5 minutes.", "edit")

        return is_valid

    # we reference the class itself and not the object when we have @classmethod as the decorator

    def is_liked_at_by(self, user_id):
        """Will return true or false if user liked a shake"""

        has_liked = False
        likes = Like.get_all_by_shake_id(self.id)
        # li = like, just had to rename since app would crash
        for li in likes:
            if li.user_id == user_id:
                has_liked = True
        return has_liked

    @classmethod
    def create(cls, form_data):
        """INSERTS a new shake in the database."""

        query = """
        INSERT INTO shakes (name, description, instructions, difficulty, is_under_5, user_id)
        VALUES (%(name)s, %(description)s, %(instructions)s, %(difficulty)s, %(is_under_5)s, %(user_id)s);
        """
        shake_id = connectToMySQL(DATABASE).query_db(query, form_data)
        return shake_id

    @classmethod
    def get_all_with_users(cls):
        """Gets all the shake rows from the database including the users who created them."""

        query = """
        SELECT * FROM shakes
        JOIN users
        ON shakes.user_id = users.id;
        """

        results = connectToMySQL(DATABASE).query_db(query)

        shakes = []

        for result in results:
            shake = Shake(result)
            creator = User.get_by_user_id(result["user_id"])

            shake.user = creator
            shakes.append(shake)

        return shakes

    @classmethod
    def get_one_with_user(cls, shake_id):
        """Gets one shake row from the database including the individual user who created it."""

        query = """
        SELECT * FROM shakes
        JOIN users
        ON shakes.user_id = users.id
        WHERE shakes.id = %(shake_id)s;
        """

        data = {"shake_id": shake_id}
        results = connectToMySQL(DATABASE).query_db(query, data)
        shake = Shake(results[0])
        creator = User.get_by_user_id(results[0]["user_id"])
        shake.user = creator

        return shake

    @classmethod
    def update_shake(cls, form_data):
        """Updates one shake row in the database."""

        query = """
        UPDATE shakes
        SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, difficulty = %(difficulty)s, is_under_5 = %(is_under_5)s
        WHERE id = %(shake_id)s;
        """
        connectToMySQL(DATABASE).query_db(query, form_data)
        return

    @classmethod
    def delete_likes(cls, shake_id):
        """Deletes one shake row in the database."""

        query = """
        DELETE FROM likes
        WHERE shake_id = %(shake_id)s;
        """

        data = {"shake_id": shake_id}

        connectToMySQL(DATABASE).query_db(query, data)
        return

    @classmethod
    def delete_shake(cls, shake_id):
        """Deletes one shake row in the database."""

        query = """
        DELETE FROM shakes
        WHERE id = %(shake_id)s;
        """

        data = {"shake_id": shake_id}

        connectToMySQL(DATABASE).query_db(query, data)
        return
