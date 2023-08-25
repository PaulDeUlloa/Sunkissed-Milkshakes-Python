from flask import flash
from flask_app.models.user import User
from flask_app.config.mysqlconnection import connectToMySQL


DATABASE = "python_project"

# (*****Change Like***)


class Like:
    def __init__(self, data):
        self.user_id = data["user_id"]
        self.shake_id = data["shake_id"]

    @classmethod
    def create_like(cls, form_data):
        """INSERTS a new like in the database."""

        query = """
        INSERT INTO likes (user_id, shake_id)
        VALUES (%(user_id)s, %(shake_id)s);
        """
        like_id = connectToMySQL(DATABASE).query_db(query, form_data)
        return like_id

    @classmethod
    def get_all_by_shake_id(cls, shake_id):
        """Gets all the like rows from the database including the users who created them."""

        query = """
        SELECT * FROM likes
        WHERE shake_id = %(shake_id)s;
        """
        data = {"shake_id": shake_id}

        results = connectToMySQL(DATABASE).query_db(query, data)

        likes = []

        for result in results:
            like = Like(result)
            likes.append(like)

        return likes

    @classmethod
    def get_like_count(cls, shake_id):
        """will return the like count"""

        query = """
        SELECT COUNT(shake_id) as 'count'
        FROM likes
        WHERE shake_id = %(shake_id)s;
        """

        data = {"shake_id": shake_id}

        results = connectToMySQL(DATABASE).query_db(query, data)
        return results[0]["count"]
