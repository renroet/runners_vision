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

# app.route('/race/<int:user_race_id>')
#   """If a user has selected a race as active, then they can log their runs for that race
#   and keep track of their trainin"""
#   """It will also have a countdown "
#   """Will have a calender-like planner on the page that will show all the completed 
#   training. Users can also click the days (tiles) of the calender to add training they 
#   have completed -- app.route('/race/<int:user_race_id>/training/add) """

# app.route('/race/<int:user_race_id>/training/add)
#   """training can also be deleted if added in error"""

# ############ AUTHENTICATION SHOULD BE IMPLIMENTED FOR ALL ADDED/DELETED TRAINING ############























