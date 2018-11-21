
import os

from flask import Flask, request, session, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from jinja2 import StrictUndefined

from model import connect_to_db, User
import auth


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "onomatopoeia")
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template('home.html')


#######################
##### route stubs #####

@app.route("/signup", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return auth.register_user(request)

    ### Display sign up form
    return render_template('signup.html')
    # return "Sign Up"


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return auth.validate_login(request)

    ### Display sign in form
    # return render_template('signin.html')
    return "Log In"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/log", methods=['GET', 'POST'])
def log_activity():
    if request.method == 'POST':
        return store_log(request)
    return "Log activity"


@app.route("/lists")
def display_lists():

    return "All Your Lists"


@app.route("/lists/<list_id>")
def display_list_items(list_id):

    return f"This is list #{list_id}"


@app.route("/items/<item_id>")
def list_activity(item_id):
    return f"Activity history of item #{item_id}"




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)


    # Use the DebugToolbar
    DebugToolbarExtension(app)

    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)

