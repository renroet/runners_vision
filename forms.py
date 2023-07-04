from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, StringField, PasswordField, TextAreaField, BooleanField, SelectField
from wtforms.validators import InputRequired, DataRequired, Email, Length, Optional, URL


WORKOUTS = ['run', 'bicycle', 'swim', 'walk', 'weight train', 'cross train']
UNITS = ['miles', 'km', 'meters']

class UserForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8), InputRequired()])
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    email = StringField('Email:', validators=[InputRequired(), Email()])
    bio = TextAreaField('(Optional) About:', validators=[Optional()])
    is_public = BooleanField('Race Board:')
    header_image_url = StringField('Header Image:', validators=[Optional(), URL()]) 
    profile_image_url = StringField('Header Image:', validators=[Optional(), URL()]) 

class UserEditForm(FlaskForm):
    """Form for editing users."""
    username = StringField('Username:', validators=[DataRequired()])
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    email = StringField('Email:', validators=[InputRequired(), Email()])
    bio = TextAreaField('(Optional) About:', validators=[Optional()])
    is_public = BooleanField('Race Board:')
    header_image_url = StringField('Header Image:', validators=[Optional(), URL()]) 
    profile_image_url = StringField('Header Image:', validators=[Optional(), URL()]) 

class TrainingForm(FlaskForm):
    """Form for adding training to race"""
    title = StringField('Title:', validators=[DataRequired()])
    body = TextAreaField('(Optional) About workout:', validators=[Optional(), Length(max=300)])
    time_spent = IntegerField('Time (in minutes):', validators=[Optional()])
    type = SelectField('Select type of worout:', choices=WORKOUTS)
    distance = FloatField('Distance:', validators=[Optional()])
    units = SelectField('Units:', choices=UNITS, default='run')


