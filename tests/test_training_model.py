"""Training model tests."""

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


class TrainingModelTestCase(TestCase):
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

        u = db.one_or_404(db.select(User).filter_by(username='testuser1'))
        r = db.one_or_404(db.select(Race).filter_by(name='test_race'))

        u.races.append(r)

        db.session.add(u)
        db.session.commit()


    def test_training_model(self):
        """Does basic model work?"""
        u = db.one_or_404(db.select(User).filter_by(username='testuser1'))
        u_r = db.one_or_404(db.select(User_Race).filter_by(user_id=u.id))
        t = Training(
            users_races_id=u_r.id,
            title='test_training1',
            type='run'
            )
        
        db.session.add(t)
        db.session.commit()

        self.assertTrue(t.id)


    def test_add_training_invalid_user_race(self):
        """Does model hinder the addition of trainings when user_race id is invalid"""
        t = Training(
            users_races_id=0,
            title='test_training1',
            type='run'
            )
        db.session.add(t)

        try:
            db.session.commit()
            raise AssertionError
        except:
            db.session.rollback()
            pass


    def test_training_in_user_race(self):
        """Does model track trainings associated with specific user's races"""
        u = db.one_or_404(db.select(User).filter_by(username='testuser1'))
        u_r = db.one_or_404(db.select(User_Race).filter_by(user_id=u.id))
        t = Training(
            users_races_id=u_r.id,
            title='test_training1',
            type='run'
            )
        
        db.session.add(t)
        db.session.commit()

        u_r.trainings.append(t)
        db.session.add(u_r)
        db.session.commit()

        self.assertEqual(len(u_r.trainings), 1)
        self.assertEqual(u_r, t.race)

    



