import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

##############################################################################
# Model definitions

class User(db.Model):
    """User information"""

    __tablename__ = "users"

    uid = db.Column(db.Integer, autoincrement=False, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    pw = db.Column(db.Binary(60), nullable=False)
    name = db.Column(db.String(64), nullable=False)

    def generate_id(self):

        #TODO: add retry logic to check for duplicates
        return int(datetime.utcnow().timestamp())

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.uid} email={self.email}>"


class List(db.Model):
    """List information"""

    __tablename__ = "lists"

    list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'))
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    desc = db.Column(db.String(280), nullable=True)
    archived = db.Column(db.Boolean, default=False)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("lists", order_by=date_created))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<List list_id={self.list_id} name={self.name} user_id={self.user_id}>"


class Item(db.Model):
    """List Item information"""

    __tablename__ = "items"

    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.list_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'))
    name = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(280), nullable=True)
    hidden = db.Column(db.Boolean, default=False)
    last_active = db.Column(db.DateTime, nullable=False)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("items", order_by=last_active))

    # Define relationship to parent list
    in_list = db.relationship("List",
                           backref=db.backref("items", order_by=item_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Item item_id={self.item_id} name={self.name} user_id={self.user_id}>"


class Activity(db.Model):
    """Activity log for a list item"""

    __tablename__ = "activity"

    activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'))
    date_logged = db.Column(db.DateTime, nullable=False)
    comment = db.Column(db.Text, nullable=True)


    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("activity", order_by=date_logged))

    # Define relationship to list item
    for_item = db.relationship("Item",
                           backref=db.backref("activity", order_by=date_logged))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Activity activity_id={self.activity_id} date_logged={self.date_logged} user_id={self.user_id} item_id={self.item_id}>"





##############################################################################
# DB Config

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "postgresql:///tada")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    db.create_all()
    db.session.commit()

    print("Connected to DB.")