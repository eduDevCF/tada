from flask import session, flash, redirect
from datetime import datetime

from server import bcrypt
from model import db, User



##############################################################################
# auth helper functions

def register_user(request):
    name = request.form["name"] #name should be less than 64 chars
    email = request.form["email"] #email should be valid (fe)
    pw = request.form["pw"] #password and pw_confirm should match

    pw_hash = bcrypt.generate_password_hash(pw)
    uid = int(datetime.utcnow().timestamp())

    new_user = User(name=name, email=email, pw=pw_hash, uid=uid)

    db.session.add(new_user)
    db.session.commit()

    flash("Your account has been created. Now just log in!")
    return redirect("/")


def validate_login(request):

    email = request.form["email"]
    pw = request.form["pw"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")


    if bcrypt.check_password_hash(user.pw, pw):
        session["user"] = {
            'name': user.name,
            'email': user.email,
            'id': user.uid
        }
        flash(f"Hi {session['user']['name']}! You're now logged in.")
    else:
        flash("Incorrect password")

    return redirect("/")


