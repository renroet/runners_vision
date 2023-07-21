"""Training view tests."""

import os
from unittest import TestCase

from models import db, User, Race, User_Race, Training

os.environ['DATABASE_URL'] = "postgresql:///runners_vision-test"

from app import app
from app import app, CURR_USER_KEY
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class TrainingViewTestCase(TestCase):
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

        testuser.races.append(r1)
        db.session.add(testuser)
        db.session.commit()

        u_r = db.one_or_404(db.select(User_Race).filter_by(user_id=testuser.id))
        u_r.is_active = True
        t = Training(
            users_races_id=u_r.id,
            type='run'
            )
        db.session.add(u_r)
        db.session.commit()
        db.session.add(t)
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


    def test_show_training(self):
        """Does app populate trainings on user profile"""
        with self.client as c:
            with c.session_transaction() as sess:
                t1 = db.one_or_404(db.select(User).filter_by(username='testuser1'))
                sess[CURR_USER_KEY] = t1.id
                    
                
            resp = c.get(f'/user/{t1.id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Training</li>', html)


    def test_add_training_form(self):
        """Does app display add training form for user"""
        with self.client as c:
            with c.session_transaction() as sess:
                t1 = db.one_or_404(db.select(User).filter_by(username='testuser1'))
                u_r1 = db.one_or_404(db.select(User_Race).filter_by(user_id=t1.id))
                sess[CURR_USER_KEY] = t1.id
                    
                
            resp = c.get(f'/race/{u_r1.id}/trainings')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<form class="form-horizontal" id="training-form" method="POST">', html)

    def test_add_training(self):
        """Does app allow user to add training"""
        with self.client as c:
            with c.session_transaction() as sess:
                t1 = db.one_or_404(db.select(User).filter_by(username='testuser1'))
                u_r1 = db.one_or_404(db.select(User_Race).filter_by(user_id=t1.id))
                sess[CURR_USER_KEY] = t1.id
                    
                
            resp = c.post(f'/race/{u_r1.id}/trainings', data={'type':'run', 'title':'Run'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Run</li>', html)

    
    def test_inactivate_race_remove_training(self):
        """Does app remove training from view when associated race is inactivated"""
        with self.client as c:
            with c.session_transaction() as sess:
                t1 = db.one_or_404(db.select(User).filter_by(username='testuser1'))
                u_r1 = db.one_or_404(db.select(User_Race).filter_by(user_id=t1.id))
                sess[CURR_USER_KEY] = t1.id
                
                u_r1.is_active=False
                db.session.add(u_r1)
                db.session.commit()
                
            resp = c.get(f'/user/{t1.id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Training</li>', html)
