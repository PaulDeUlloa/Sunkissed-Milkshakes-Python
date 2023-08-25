from flask_app import app

# DONT FORGET TO INPUT CONTROLLERS HERE
import flask_app.controllers.users
import flask_app.controllers.shakes
import flask_app.controllers.likes

# Add other table name ABOVE^

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8018)
