from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """Users."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    username = db.Column(db.String(50),
                    nullable=False,
                    unique=True)
    password = db.Column(db.String,
                    nullable=False)
    first_name = db.Column(db.String(30),
                            nullable=False)
    last_name = db.Column(db.String(30),
                            nullable=False)
    bio = db.Column(db.String(300))
    email = db.Column(db.String,
                      nullable=False,
                      unique=True)
    is_public = db.Column(db.Boolean,
                        nullable=False,
                        default=True)
    header_image_url = db.Column(db.Text,
                                nullable=False,
                                default='https://img.freepik.com/premium-vector/abstract-light-blue-blurred-background_444390-12861.jpg')
    profile_image_url = db.Column(db.Text,
                                nullable=False,
                                default='https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg')
    created_at = db.Column(db.DateTime,
                            default=datetime.utcnow,
                            nullable=False)
    
    races = db.relationship('Race',
                            single_parent=True,
                            secondary="users_races",
                            cascade='all, delete, delete-orphan',
                            backref="trainees")


    @classmethod
    def signup(cls, username, email, password, first_name, last_name):
        """creates instance of user and password"""
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
                username=username,
                email=email,
                password=hashed_pwd,
                first_name=first_name,
                last_name=last_name
            )

        db.session.add(user)

        return user

    @classmethod
    def authenticate(cls, username, password):
        """compares username and password provided with users in db"""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
# 
# 

class Race(db.Model):
    """Races."""

    __tablename__ = "races"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    name = db.Column(db.String(80),
                    nullable=False)
    city = db.Column(db.String)
    state = db.Column(db.String)
    info = db.Column(db.Text)
    image_url = db.Column(db.Text,
                                nullable=False,
                                default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdX_uUSvKmz2ITnpw8W5VVJQzqEdOxUrlW1Q&usqp=CAU')
    start_date = db.Column(db.String,
                            nullable=False)           

class User_Race(db.Model):
    """Users Races."""

    __tablename__ = "users_races"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    race_id = db.Column(db.Integer,
                        db.ForeignKey('races.id', ondelete="cascade"),
                        nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete="cascade"),
                        nullable=False)
    is_active = db.Column(db.Boolean,
                        nullable=False,
                        default=False)
    is_complete = db.Column(db.Boolean,
                        nullable=False,
                        default=False)
    trainings = db.relationship('Training',
                            cascade='all, delete, delete-orphan',
                            backref='race')

    def deactivate(cls):
            """"deactivate races in users races upon the activation of a new one"""

            cls.is_active = False

            db.session.commit()
            return 

    
class Training(db.Model):
    """Trainings."""

    __tablename__ = "trainings"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    users_races_id = db.Column(db.Integer,
                        db.ForeignKey('users_races.id'),
                        nullable=False)
    title = db.Column(db.String(30),
                    nullable=False,
                    default='Training')
    body = db.Column(db.String(300))
    time_spent = db.Column(db.Integer)
    type = db.Column(db.String(20),
                    nullable=False)
    distance = db.Column(db.Float)
    units = db.Column(db.String(6))
    created_at = db.Column(db.DateTime,
                        nullable=False,
                        default=datetime.utcnow())

#     songs = db.relationship("Song", 
#                             secondary='playlist_songs',
#                             backref='playlists')


# class Song(db.Model):
#     """Song."""

#     __tablename__ = "songs"

