from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, FloatField, StringField, PasswordField, TextAreaField, BooleanField, SelectField
from wtforms.validators import InputRequired, DataRequired, Email, Length, Optional, URL


WORKOUTS = ['run', 'bicycle', 'swim', 'walk', 'weight train', 'cross train']
UNITS = ['miles', 'km', 'meters']
RACEUNITS = [('K', 'Kilometers'),('M','Miles'), ('y','Yards'),('m', 'Meters')]
TYPE = [('running_race', 'Run'), ('triathlon', 'Triathlon'), ('trail_race', 'Trail Race')]

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8), InputRequired()])
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    email = StringField('Email:', validators=[InputRequired(), Email()])
   
class UserEditForm(FlaskForm):
    """Form for editing users."""
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8), InputRequired()])
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    email = StringField('Email:', validators=[InputRequired(), Email()])
    bio = TextAreaField('(Optional) About:', validators=[Optional()])
    is_public = BooleanField('Public:', default=True)
    header_image_url = StringField('Header Image:', validators=[Optional(), URL()]) 
    profile_image_url = StringField('Profile Image:', validators=[Optional(), URL()]) 

class TrainingForm(FlaskForm):
    """Form for adding training to race"""
    title = StringField('Title:', validators=[DataRequired()])
    body = TextAreaField('(Optional) About workout:', validators=[Optional(), Length(max=300)])
    time_spent = IntegerField('Time (in minutes):', validators=[Optional()])
    type = SelectField('Select type of worout:', choices=WORKOUTS, default='run')
    distance = FloatField('Distance:', validators=[Optional()])
    units = SelectField('Units:', choices=UNITS, default='miles')

class LoginForm(FlaskForm):
    """Form for logging in a known user"""
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8), InputRequired()])

class SearchRacesForm(FlaskForm):
    """Form for searching races in API/db"""
    username = StringField('Username:', validators=[Optional(), Length(max=100)])
    name = StringField('Name:', validators=[Optional(), Length(max=100)])
    start_date = DateField('Date:', validators=[Optional()], description='YYYY-MM-DD')
    city = StringField('City:', validators=[Optional()])
    state = StringField('State:', validators=[Optional()])
    max_distance = FloatField('Distance:', validators=[Optional()])
    distance_units =  SelectField('Units:', choices=RACEUNITS, validators=[Optional()])
