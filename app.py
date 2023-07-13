# app.route('/')
# def homepage():
#   """Homepage offering user login or signup option"""
#   """Can also begin exploring races from this page. However, cannot commit any races
#       vision board without being logged in"""
#   """"Renders template with form in style of search bar to look for races"""
#   """Maybe have some pre-linked links on homepage to grouped race searches to get users 
#   started"""

# app.route('/races')
# def show_all_races():
#   """Calls api and shows the 50 races coming up next by default"""
#   """Renders an Index template that changes with the user filter search"""
#   """Form style search bar like in homepage"

# app.route('/races/<int:race_id>)
# def show_race_info():
#   """Shows all information about a race from the API"""
#   """This is where user can select race to be on their vision board"""

# app.route('/login')
#   """Need and authentication in the user model"""

# app.route('/logout')

# app.route('/user/<int:user_id>/races')
#   """Displays all races user has put on their vision board"""
#   """User can select one to be an active race that they are training for"""
#   """When a race becomes active it is given a different set of interactions in the main
#   user profile"""

# app.route('/user/<int:user_id>')
#   """Display user profile. Have active race heading a field and race countdown"""
#   """Have a spot for completed races. Possibly with medals to indicate completion."""
#   """Flashes occur at important times to inform user about upcoming moments and training"""
#   """Spot for weekly sum of miles run may also be good"""

# app.route('/race/<int:users_races_id>')
#   """If a user has selected a race as active, then they can log their runs for that race
#   and keep track of their trainin"""
#   """It will also have a countdown "
#   """Will have a calender-like planner on the page that will show all the completed 
#   training. Users can also click the days (tiles) of the calender to add training they 
#   have completed -- app.route('/race/<int:user_race_id>/training/add) """

# app.route('api/race/<int:users_races_id>/training/add)
#   """training can also be deleted if added in error"""

# ############ AUTHENTICATION SHOULD BE IMPLIMENTED FOR ALL ADDED/DELETED TRAINING ############

# app.route('api/race/<int:users_races_id>/training/delete)
#   """training can also be deleted if added in error"""

# #### trainings will be validated and added into db using wtforms ######

# app.route('api/race/<int:users_races_id>')......or maybe just an UPDATE PATCH
# """PATCH to update to completed or inactive/active"

# make api to: 
#   - create "users_races"
#   - update "users_races" as completed, active, or inactive
#   - delete "users_races"
#   - create "users_races" - "training"
#   - delete "users_races" - "training"
#   - create "user"
#   - update "user" to private/public
#   - delete "user"



from flask import Flask, render_template, request, jsonify, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests 
from json import JSONDecodeError

from forms import UserAddForm, UserEditForm, TrainingForm, LoginForm, SearchRacesForm
from models import db, connect_db, User, Training, Race, User_Race

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.app_context().push()
# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///runners_vision'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "it's a secret"
toolbar = DebugToolbarExtension(app)

connect_db(app)



@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = db.session.execute(db.select(User).filter_by(id=(session[CURR_USER_KEY]))).scalar()

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash('Logged out', 'success')
    return redirect('/login')


@app.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """Render edit user form and update user"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = UserEditForm(obj=g.user)

    if form.validate_on_submit():
        user = User.authenticate(g.user.username,
                                 form.password.data)
        if user:
        
            g.user.username=form.username.data,
            g.user.password=form.password.data,
            g.user.email=form.email.data,
            g.user.header_image_url=form.header_image_url.data or User.header_image_url.defaularg,
            g.user.profile_image_url=form.profile_image_url.data or User.profile_image_url. defaularg,
            g.user.first_name=form.first_name.data,
            g.user.last_name=form.last_name.data,
            g.user.bio=form.bio.data,
            g.user.is_public=form.is_public.data

            db.session.commit()

            flash(f'{g.user.username} updated', 'success')
            return redirect(f'/user/{g.user.id}')
        
        flash('Invalid credentials', 'danger')
        return redirect('/')

    return render_template('edit_user.html', form=form)



@app.route('/')
def homepage():
    """display homepage with login/signup options"""
    return redirect('/races')

@app.route('/races')
def show_all_races():
    """Calls api and shows the 50 races coming up next by default"""
    
    user_id = g.user.id if g.user else 0

    resp = requests.get('https://runsignup.com/rest/races', params={'format': 'json'})
    data = resp.json()
    races = data['races']
    html = ['<', '>', '</', 'span>', 'b>', 'p>', 'a>', 'href', 'ul>']
    race = 'race'
    name = 'name'
    date = 'next_date'
    address = 'address'
    link = 'url'
    description = 'description'
 
   
    return render_template('show.html', data=data, races=races, race=race, name=name, date=date, address=address, link=link, description=description, html=html, user_id=user_id)

@app.route('/races/search', methods = ['GET', 'POST'])
def search_races():
    """Renders form and calls api with form info"""

    form = SearchRacesForm()
    search = {'format': 'json'}
    if form.validate_on_submit():
        name = form.name.data
        if name:
            search.update({'name': name})
        start_date = form.start_date.data
        if start_date:
            search.update({'start_date': start_date})
        city = form.city.data
        if city:
            search.update({'city': city})
        state = form.state.data
        if state:
            search.update({'state': state})
        max_distance = form.max_distance.data
        if max_distance:
            search.update({'max_distance': max_distance})
        distance_units = form.distance_units.data
        if distance_units:
            search.update({'distance_units': distance_units})
     
        resp = requests.get('https://runsignup.com/rest/races', params=search)
    
        data = resp.json()
        races = data['races']
        if not races:
            flash('There are no races matching the criteria', 'error')
            return render_template('search.html', form=form)
        html = ['<', '>', '</', 'span>', 'b>', 'p>', 'a>', 'href', 'ul>']
        race = 'race'
        name = 'name'
        date = 'next_date'
        address = 'address'
        link = 'url'
        description = 'description'

        user_id = g.user.id if g.user else 0

        return render_template('show.html', data=data, races=races, race=race, name=name,  date=date, address=address, link=link, description=description, html=html, user_id=user_id)

       
    return render_template('search.html', form=form)

@app.route('/user/<int:user_id>/races/add', methods=['GET', 'POST'])
def add_race(user_id):
    """add race to user in db""" 
    if not g.user or user_id == 0:
        flash("Must be logged in", "danger")
        return redirect("/")


    name = request.form["name"]

    for r in g.user.races:
        if r.name == name:
            return redirect('/races')

    resp = requests.get('https://runsignup.com/rest/races', params={'format': 'json', 'name': name})

#     for i in data['races']:
# ...   if i['race']['race_id'] == 146508:
# ...     print(i)

    data = resp.json()
    race = data['races'][0]['race']

    name = race['name']
    city = race['address']['city']
    state = race['address']['state']
    start_date = race['next_date']

    race = Race(name=name, city=city, state=state, start_date=start_date)

    db.session.add(race)
    db.session.commit()

    g.user.races.append(race)

    db.session.add(g.user)
    db.session.commit()

    # u_race = db.session.execute(db.select(User_Race).filter_by(race_id=race.id)).scalar_one()


    return render_template('activate.html', name = name, user_id=user_id, race_id=race.id)

    # name = db.Column(db.String(80),
    #                 nullable=False)
    # info = db.Column(db.Text)
    # image_url = db.Column(db.Text,
    #                             nullable=False,
    #                             default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdX_uUSvKmz2ITnpw8W5VVJQzqEdOxUrlW1Q&usqp=CAU')
    # start_date = db.Column(db.String,
    #                         nullable=False)           

    return redirect('/')
# if form.validate_on_submit():
#         user = User.authenticate(g.user.username,
#                                  form.password.data)
#         if user:
#             g.user.username = form.username.data
#             g.user.email = form.email.data
#             g.user.image_url = form.image_url.data
#             g.user.header_image_url = form.header_image_url.data
#             g.user.bio = form.bio.data

#             db.session.commit()
#             flash(f'{g.user.username} updated', 'success')
#             return redirect(f'/users/{g.user.id}')
        
#         flash('Invalid credentials', 'danger')
#         return redirect('/')

#     return render_template('/users/edit.html', form=form)

@app.route('/races/<int:user_id>/<int:race_id>/activate', methods=['POST'])
def set_active_status(user_id, race_id):
    """sets the newly added race as either active or inactive"""
    
    races = g.user.races

    for r in races:
        r = db.session.execute(db.select(User_Race).filter_by(race_id=r.id, user_id = g.user.id)).scalar_one()

        r.deactivate()

    u_race = db.session.execute(db.select(User_Race).filter_by(race_id=race_id, user_id=user_id)).scalar_one()
    # race = db.session.execute(db.select(Race).filter_by(id=u_race.race_id)).scalar_one()
    u_race.is_active = True 

    db.session.commit()
    
    return redirect(f'/user/{user_id}')

@app.route('/user/<int:user_id>')
def user_profile(user_id):
    """Display user profile. Have active race heading a field and race countdown"""
    """Have a spot for completed races. Possibly with medals to indicate completion."""
    """Flashes occur at important times to inform user about upcoming moments and training"""
    """Spot for weekly sum of miles run may also be good"""

    if not g.user.id == user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    race = ''
    u_r = db.session.execute(db.select(User_Race).filter_by(is_active=True, user_id = g.user.id)).scalar()
    if u_r:
        r = db.session.execute(db.select(Race).filter_by(id = u_r.race_id)).scalar()
        race = r.name

    trainings = []
    total_run_m = 0
    total_bike_m = 0
    total_walk_m = 0
    if u_r:
        trainings = u_r.trainings
        for t in trainings:
            v = t.type
            if v == 'run' and t.distance:
                d = float(t.distance)
                if t.units == 'meters':
                    d = t.distance / 1609
                if t.units == 'km':
                    d = t.distance/1.609
                total_run_m = total_run_m + d
            if v == 'bicycle' and t.distance:
                d = float(t.distance)
                if t.units == 'meters':
                    d = t.distance / 1609
                if t.units == 'km':
                    d = t.distance/1.609
                total_bike_m = total_bike_m + d
            if v == 'walk' and t.distance:
                d = float(t.distance)
                if t.units == 'meters':
                    d = t.distance / 1609
                if t.units == 'km':
                    d = t.distance/1.609
                total_walk_m = total_walk_m + d

    return render_template('profile.html', user=user, race=race, trainings=trainings, u_r=u_r, total_r=round(total_run_m), total_b=round(total_bike_m), total_w=round(total_walk_m))
    

@app.route('/user/<int:user_id>/races')
def show_user_races(user_id):
    if not g.user.id == user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    races = g.user.races
    return render_template('user_races.html', user=user, races=races)



@app.route('/race/<int:users_races_id>/trainings', methods=['GET', 'POST'])
def add_training(users_races_id):
    """Render TrainingForm. Add training to users_races table in db."""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = TrainingForm()

    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        time_spent = form.time_spent.data
        type = form.type.data
        distance = form.distance.data
        units = form.units.data
    
        t = Training(users_races_id=users_races_id, title=title, body=body, time_spent=time_spent, type=type, distance=distance, units=units)

        db.session.add(t)
        db.session.commit()

        return redirect(f'/user/{g.user.id}')

    return render_template('add_training.html', form=form)