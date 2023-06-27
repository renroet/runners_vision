import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class Users(db.Model):
    """Users."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    username = db.Column(db.String(50),
                    nullable=False)
    first_name = db.Column(db.String(30),
                            nullable=False)
    last_name = db.Column(db.String(30),
                            nullable=False)
    bio = db.Column(db.String(300))
    email = db.Column(db.String,
                      nullable=False)
    is_public = db.Column(db.Boolean,
                        nullable=False,
                        default=True)
    header_image_url = db.Column(db.Text,
                                nullable=False,
                                default='https://img.freepik.com/premium-vector/abstract-light-blue-blurred-background_444390-12861.jpg')
    profile_image_url = db.Column(db.Text,
                                nullable=False,
                                default='https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg')
    created_at = db.Column(db.Datetime,
                            default=datetime.datetime.utcnow,
                            nullable=False)
# 
# 
#     songs = db.relationship("Song", 
#                             secondary='playlist_songs',
#                             backref='playlists')


# class Song(db.Model):
#     """Song."""

#     __tablename__ = "songs"

