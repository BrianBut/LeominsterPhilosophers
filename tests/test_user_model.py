import unittest
import time
from datetime import datetime
from app import create_app, db
from app.models import User, AnonymousUser, Role, Permission


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_invalid_reset_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertFalse(User.reset_password(token + 'a', 'horse'))
        self.assertTrue(u.verify_password('cat'))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.READ))
        self.assertFalse(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_timestamp(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        self.assertTrue(
            (datetime.utcnow() - u.last_seen).total_seconds() < 3)

    def test_ping(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        time.sleep(2)
        last_seen_before = u.last_seen
        u.ping()
        self.assertTrue(u.last_seen > last_seen_before)
    '''
    def test_is_administrator(self):
        r = Role.query.filter_by(name='Moderator').first()
        u = User(email='john@example.com', password='cat', role=r)
        self.assertFalse( u.is_administrator() )

        r = Role.query.filter_by(name='Administrator').first()
        u = User(email='jill@example.com', password='cat', role=r)
        self.assertTrue( u.is_administrator() )

    def test_is_moderator(self):
        r = Role.query.filter_by(name='Moderator').first()
        u = User(email='john@example.com', password='cat', role=r)
        self.assertFalse( u.is_administrator() )
        self.assertTrue( u.is_moderator() )
        self.assertTrue( u.can(Permission.READ) )
        self.assertTrue( u.can(Permission.WRITE) )

    def test_is_guest(self):
        u = User(email='john@example.com', password='cat')
        self.assertFalse( u.is_administrator() )
        self.assertFalse( u.is_moderator() )
        self.assertTrue( u.can(Permission.READ) )
        self.assertFalse( u.can(Permission.WRITE) )
    '''
    def test_fullname(self):
        r = Role.query.filter_by(name='User').first()
        u = User(email='john@example.com', password='cat', first_name='Rosy', last_name='Lee', role=r)
        self.assertTrue( u.fullname() == 'Rosy Lee')

    def test_has_valid_profile(self):
        r = Role.query.filter_by(name='User').first()
        u1 = User(email='johnsmith@example.com', password='cat', first_name='Rosy', last_name='Lee', role=r)
        self.assertTrue( u1.has_valid_profile() )
        u2 = User(email='john@example.com', password='cat', first_name='R', last_name='L')
        self.assertFalse( u2.has_valid_profile() )

    def test_no_profile_is_invalid(self):
        u = User(email='john@example.com', password='cat')
        print(u.first_name)
        print(u.last_name)
        print(u.fullname())
        self.assertFalse( u.has_valid_profile() )
'''
    def test_to_json(self):
        u = User(email='john@example.com', password='cat')
        db.session.add(u)
        db.session.commit()
        with self.app.test_request_context('/'):
            json_user = u.to_json()
        expected_keys = ['url', 'username', 'member_since', 'last_seen']
        self.assertEqual(sorted(json_user.keys()), sorted(expected_keys))
        self.assertEqual('/api/v1/users/' + str(u.id), json_user['url'])
'''