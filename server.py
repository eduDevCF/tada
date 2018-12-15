
import os

from flask import Flask, request, session, redirect, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from jinja2 import StrictUndefined
from datetime import datetime

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


@app.route("/list", methods=['POST'])
def create_new_list():

    user = session.get("user")
    list_name = request.form["name"]
    timestamp = datetime.now()

    new_list = List(user_id=user.id, name=list_name, date_created=timestamp)
    #TODO: Error Handling
    db.session.add(new_list)
    db.session.commit()

    return redirect("/list/" + td_list.list_id)



@app.route("/list/<int:list_id>", methods=['GET', 'POST'])
def list_requests(list_id):

    user = session.get("user")
    td_list = List.query.get(list_id)

    if user.id != td_list.user_id:
        return "Error: Access Denied" #TODO: better error handling

    if request.method == 'POST':
        return update_list(request, td_list)

    return jsonify(td_list) #should include items; need to check that it does



def update_list(request, td_list):

    name = request.form['name']
    desc = request.form['desc']
    archive = request.form['archive']

    if name:
        td_list.name = name
    if desc:
        td_list.desc = desc
    if archive:
        return archive_list(td_list) #TODO

    db.session.add(td_list)
    db.session.commit()

    return (jsonify(td_list))



@app.route("/item", methods=['POST'])
def create_new_item():

    user = session.get("user")
    list_id = request.form["list_id"]
    item_name = request.form["name"]
    timestamp = datetime.now()

    new_item = Item(user_id=user.id, list_id=list_id, name=item_name, last_active=timestamp)
    #TODO: Error Handling
    db.session.add(new_item)
    db.session.commit()

    return jsonify(new_item)



@app.route("/item/<int:item_id>", methods=['GET', 'POST'])
def item_requests(item_id):

    user = session.get("user")
    item = Item.query.get(item_id)

    if user.id != item.user_id:
        return "Error: Access Denied" #TODO: better error handling

    if request.method == 'POST':
        return update_item(request, item)

    return jsonify(item) #should include activity; need to check that it does



def update_item(request, item):

    name = request.form['name']
    desc = request.form['desc']
    should_hide = request.form['hide']
    timestamp = datetime.now()

    if name:
        item.name = name
    if desc:
        item.desc = desc
    if should_hide:
        item.hidden = should_hide

    db.session.add(item)
    db.session.commit()

    return (jsonify(item))



@app.route("/activity", methods=['POST'])
def log_new_activity():

    user = session.get("user")
    item_id = request.form["item_id"]
    timestamp = datetime.now()

    new_activity = Activity(user_id=user.id, item_id=item_id, last_active=timestamp)
    #TODO: Error Handling
    db.session.add(new_activity)
    db.session.commit()

    return jsonify(new_activity)



@app.route("/activity/<int:activity_id>", methods=['GET', 'POST'])
def activity_requests(activity_id):

    user = session.get("user")
    activity = Activity.query.get(activity_id)

    if user.id != activity.user_id:
        return "Error: Access Denied" #TODO: better error handling

    if request.method == 'POST':
        return update_activity(request, activity)

    return jsonify(activity)



def update_activity(request, activity):

    comment = request.form['comment']
    should_hide_item = request.form['hide']
    timestamp = request.form['timestamp'] #gonna need some strp/strftime work depending on form

    if comment:
        activity.comment = comment
    if date_logged:
        activity.date_logged = timestamp #TODO: format date/time
    if should_hide_item:
        item = Item.query.get(activty.item_id)
        item.hidden = should_hide_item
        db.session.add(item)

    db.session.add(activity)
    db.session.commit()

    return (jsonify(item))


############################
##### helper functions #####


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

