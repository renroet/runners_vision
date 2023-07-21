"""User model tests."""

import os
from unittest import TestCase

from models import db, User, Race, User_Race, Training


os.environ['DATABASE_URL'] = "postgresql:///runners_vision-test"


from app import app
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class UserModelTestCase(TestCase):
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


    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            username="testuser",
            email="test@test.com",
            password="HASHED_PASSWORD",
            first_name='test_first',
            last_name='test_last',
        )

        db.session.add(u)
        db.session.commit()

       
        self.assertEqual(len(u.races), 0)
        self.assertTrue(u.id)
    

    def test_has_races(self):
        """Does model correctly detect when a user has races added to vision board"""
        u1 = db.one_or_404(db.select(User).filter_by(username='testuser1'))  
        r1 = db.one_or_404(db.select(Race).filter_by(name='test_race'))  

        u1.races.append(r1)

        self.assertIn(r1, u1.races)
        self.assertEqual(len(u1.races), 1)

    
    def test_has_no_races(self):
        """Does model correctly detect when user has no races added to vision board"""
        u1 = db.one_or_404(db.select(User).filter_by(username='testuser1'))  
        r1 = db.one_or_404(db.select(Race).filter_by(name='test_race'))  

        self.assertNotIn(r1, u1.races)
        self.assertEqual(len(u1.races), 0)


    def test_user_signup(self):
        """Does method create new User upon signup"""
        u = User.signup('testuser3', "test@test.com", "HASHED_PASSWORD", 'test3_first', 'test3_last')
        
        self.assertTrue(u.username)
        

    def test_user_signup_validation(self):
        """Does signup fail with invalid input (repeated username in this instance)"""
        with self.client as c:
            u = User.signup('testuser2', "test@test.com", "HASHED_PASSWORD", 'test3_first', 'test3_last')
            db.session.add(u)
            try:
                db.session.commit()
                raise AssertionError
            except:
                db.session.rollback()
                pass

    def test_user_authenticate(self):
        """Is established user able to be authenticated"""
        with self.client as c:
            u = User.signup('testuser3', "test@test.com", "HASHED_PASSWORD", 'test3_first', 'test3_last')
            username = u.username
            self.assertTrue(User.authenticate(username, "HASHED_PASSWORD"))

    
    def test_username_authentication_failure(self):
        """Does authentication fail with invalid username match"""
        with self.client as c:
            u = User.signup('testuser3', "test@test.com", "HASHED_PASSWORD", 'test3_first', 'test3_last')
            
            username = 'bestuser'
            self.assertFalse(User.authenticate(username, "HASHED_PASSWORD"))
    
    def test_password_authentication_failure(self):
        """Does authentication fail with invalid password match"""
        with self.client as c:
            u = User.signup('testuser3', "test@test.com", "HASHED_PASSWORD", 'test3_first', 'test3_last')
           
            username = u.username
            self.assertFalse(User.authenticate(username, "HASHED_PAS3WORD"))

    


        