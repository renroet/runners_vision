"""Race/user_race model tests."""

import os
from unittest import TestCase
from sqlalchemy.orm.exc import NoResultFound

from models import db, User, Race, User_Race, Training

os.environ['DATABASE_URL'] = "postgresql:///runners_vision-test"

from app import app
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class RaceModelTestCase(TestCase):
    """Test models for user."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Race.query.delete()
        User_Race.query.delete()
        Training.query.delete()

        self.client = app.test_client()

        u1 = User(
            username="testuser1",
            email="test1@test.com",
            password="HASHED_PASSWORD",
            first_name='test1_first',
            last_name='test1_last'
        )
        db.session.add(u1)

        u2 =  User(
            username="testuser2",
            email="test2@test.com",
            password="HASHED_PASSWORD",
            first_name='test2_first',
            last_name='test2_last'
        )
        db.session.add(u2)
        db.session.commit()
        
        u2.is_public = False
        db.session.commit()

        r1 = Race(
            name='test_race',
            start_date='1-1-2024'
        )

        db.session.add(r1)
        db.session.commit()



    def test_race_model(self):
        """Does basic model work?"""

        r = Race(
            name='test_race1',
            start_date='1-2-2024'
        )
        

        db.session.add(r)
        db.session.commit()


    def test_race_user(self):
        """Does model track users of race?"""
        u = db.one_or_404(db.select(User).filter_by(username='testuser1'))
        r = db.one_or_404(db.select(Race).filter_by(name='test_race'))

        u.races.append(r)

        self.assertIn(u, r.trainees)


    def test_race_not_user(self):
        """Does not falsely associate users with races"""
        u = db.one_or_404(db.select(User).filter_by(username='testuser1'))
        r = db.one_or_404(db.select(Race).filter_by(name='test_race'))

        self.assertNotIn(u, r.trainees)

    
    def test_message_cascade_delete(self):
        """Does race relationship delete when user is deleted"""
        u = db.one_or_404(db.select(User).filter_by(username='testuser1'))

        db.session.delete(u)
        db.session.commit()
            
        try:
            db.session.query(User_Race).one()
        except NoResultFound:
            pass

    
    def test_race_validation_addition(self):
        """Does model hinder the addition of a race without a user"""

        u = db.one_or_404(db.select(User).filter_by(username='testuser1'))
        r = db.one_or_404(db.select(Race).filter_by(name='test_race'))
        
        u.races.append

        try:
            db.session.commit()
            raise AssertionError
        except:
            db.session.rollback()
            pass
    

    def test_race_deactivate(self):
        """Does model deactivate activated races when prompted"""

        r = db.one_or_404(db.select(Race).filter_by(name='test_race'))
        u = db.one_or_404(db.select(User).filter_by(username='testuser1'))
        u.races.append(r)
        db.session.add(u)
        db.session.commit()

        u_r = db.one_or_404(db.select(User_Race).filter_by(race_id=r.id))
        u_r.is_active=True
        db.session.commit()

        u_r.deactivate()     

        self.assertFalse(u_r.is_active) 
