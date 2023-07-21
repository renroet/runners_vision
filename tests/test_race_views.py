"""User view tests."""

# run these tests like:
#
#    python -m unittest tests/test_race_views.py


import os
from unittest import TestCase

from models import db, User, Race, User_Race, Training

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///runners_vision-test"


# Now we can import app

from app import app
from app import app, CURR_USER_KEY
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class RaceViewTestCase(TestCase):
    """Test views for races/user's races."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Race.query.delete()
        User_Race.query.delete()
        Training.query.delete()

        self.client = app.test_client()

        r1 = Race(
            name='test_race',
            start_date='1-1-2024'
        )

        db.session.add(r1)
        db.session.commit()

        testuser = User.signup(
                            username="testuser1",
                            email="test1@test.com",
                            password="HASHED_PASSWORD",
                            first_name='test1_first',
                            last_name='test1_last'
                            )
        db.session.commit()

        testuser2 =  User.signup(
                            username="testuser2",
                            email="test2@test.com",
                            password="HASHED_PASSWORD",
                            first_name='test2_first',
                            last_name='test2_last'
                            )
        db.session.commit()
        
        testuser2.is_public = False
        db.session.add(testuser2)
        db.session.commit()


    def test_show_races(self):
        """Does app populate and show next 50 races on homepage"""
        with self.client as c:
            resp = c.get(f'/races')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button class="add-sm"', html)

   
    def test_show_race_search(self):
        """Does app display race search when user logged in"""
        with self.client as c:
            with c.session_transaction() as sess:
                t2 = db.one_or_404(db.select(User).filter_by(username='testuser2'))
                sess[CURR_USER_KEY] = t2.id

            resp = c.get(f'/races/search')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<form class="form" id="search-races-form" method="POST">', html)


    def test_restrict_race_addition(self):
        """Does app hinder adding race to vision board when user not logged in"""
        with self.client as c:
            t2 = db.one_or_404(db.select(User).filter_by(username='testuser2'))

            resp = c.post(f'/user/{t2.id}/races/add', data={'name': 'test_race'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Must be logged in', html)
            self.assertNotIn('type="submit">Activate</button', html)

    
    def test_race_add(self):
        """Does add link work to add races to vision board when user logged in"""
        with self.client as c:
            with c.session_transaction() as sess:
                t2 = db.one_or_404(db.select(User).filter_by(username='testuser2'))
                sess[CURR_USER_KEY] = t2.id

            resp = c.post(f'/user/{t2.id}/races/add', data={'name': 'test_race'})
            html = resp.get_data(as_text=True)


            self.assertEqual(resp.status_code, 200)
            self.assertIn('type="submit">Activate</button', html)
            self.assertIn('<h1>test_race</h1>', html)
                    
    
    def test_add_not_auth_user(self):
        """Does app hinder the addition of races to another users account"""

        with self.client as c:
            with c.session_transaction() as sess:
                t2 = db.one_or_404(db.select(User).filter_by(username='testuser2'))
                t1 = db.one_or_404(db.select(User).filter_by(username='testuser1'))
                sess[CURR_USER_KEY] = t2.id

            resp = c.post(f'/user/{t1.id}/races/add', data={'name': 'test_race'}, follow_redirects=True)
            html = resp.get_data(as_text=True)


            self.assertEqual(resp.status_code, 200)
            self.assertIn('Access unauthorized', html)
            self.assertNotIn('type="submit">Activate</button', html)


    def test_race_activate(self):
        """Does add link work to activate added race and display on vision board"""
        with self.client as c:
            with c.session_transaction() as sess:
                r = db.one_or_404(db.select(Race).filter_by(name='test_race'))
                t2 = db.one_or_404(db.select(User).filter_by(username='testuser2'))
                sess[CURR_USER_KEY] = t2.id
                t2.races.append(r)
                db.session.add(t2)
                db.session.commit()

            resp = c.post(f'/races/{t2.id}/{r.id}/activate', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Training for: test_race</h2>', html)
            


    def test_race_activate_no_auth_user(self):
        """Does app hinder the activation of races on another user's account"""

        with self.client as c:
            with c.session_transaction() as sess:
                r = db.one_or_404(db.select(Race).filter_by(name='test_race'))
                t1 = db.one_or_404(db.select(User).filter_by(username='testuser1'))
                t2 = db.one_or_404(db.select(User).filter_by(username='testuser2'))
                sess[CURR_USER_KEY] = t2.id
                t1.races.append(r)
                db.session.add(t1)
                db.session.commit()

            resp = c.post(f'/races/{t1.id}/{r.id}/activate', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button class="add-sm"', html)
            self.assertIn('Access unauthorized.', html)



#     def test_logged_out_races(self):
#         """Does app prohibit user from seeing races of other profiles when logged out"""
#         with self.client as c:
#             t1 = db.one_or_404(db.select(User).filter_by(username='testuser1'))
                    
#             r1 = Race(
#                 name='test_race',
#                 start_date='1-1-2024'
#                 )

#             db.session.add(r1)
#             db.session.commit()

#             t1.races.append(r1)
#             db.session.add(t1)
#             db.session.commit()
#             resp = c.get(f'/user/{t1.id}/races', follow_redirects=True)
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertIn('Access unauthorized.', html)


#     def test_private_races(self):
#         """Does app prohibit user from seeing races of private profiles"""
#         with self.client as c:
#             with c.session_transaction() as sess:
#                 t2 = db.one_or_404(db.select(User).filter_by(username='testuser2'))
#                 t1 = db.one_or_404(db.select(User).filter_by(username='testuser1'))
#                 sess[CURR_USER_KEY] = t1.id
                    
#                 r1 = Race(
#                         name='test_race',
#                         start_date='1-1-2024'
#                         )

#                 db.session.add(r1)
#                 db.session.commit()

#                 t2.races.append(r1)
#                 db.session.add(t2)
#                 db.session.commit()
#             resp = c.get(f'/user/{t2.id}/races', follow_redirects=True)
#             html = resp.get_data(as_text=True)
            
#             self.assertEqual(resp.status_code, 200)
#             self.assertIn('Access unauthorized.', html)





#  with c.session_transaction() as sess:
#                 t2 = db.one_or_404(db.select(User).filter_by(username='testuser2'))
#                 t1 = db.one_or_404(db.select(User).filter_by(username='testuser1'))
#                 sess[CURR_USER_KEY] = t2.id
                    
#                 r1 = Race(
#                         name='test_race',
#                         start_date='1-1-2024'
#                         )

#                 db.session.add(r1)
#                 db.session.commit()

#                 t1.races.append(r1)
#                 db.session.add(t1)
#                 db.session.commit()