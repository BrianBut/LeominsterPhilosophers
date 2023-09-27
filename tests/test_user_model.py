import unittest
import time
from datetime import datetime
from app import create_app, db, bcrypt
from app.models import User, AnonymousUser


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(email='cat@my.bed', password='cat')
        self.assertTrue(u.password is not None)
    
    def test_password_salts_are_random(self):
        u = User(email='paws@his.house', password='cat')
        u2 = User(email='paws@his.house', password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_bcrypt_setter(self):
        pw_hash = bcrypt.generate_password_hash('hunter2')
        self.assertTrue(pw_hash is not None)
    
    def test_bcrypt_is_valid(self):
        pw_hash = bcrypt.generate_password_hash('hunter2')
        is_valid = bcrypt.check_password_hash(pw_hash, 'hunter2')
        self.assertTrue( is_valid )

    def test_bcrypt_is_invalid(self):
        pw_hash = bcrypt.generate_password_hash('hunter2')
        is_valid = bcrypt.check_password_hash(pw_hash, 'hanter2')
        self.assertFalse( is_valid )

    # Test that password_hash gets set by User.init()
    def test_password_setter(self):
        u = User(email='paws@his.house', password='cat')
        self.assertTrue(u.password_hash is not None)
    
    # Be sure there is no password attribute
    def test_no_password_getter(self):
        u = User(email='paws@his.house', password='cat')
        with self.assertRaises(AttributeError):
            u.password
    
    # Password verification works
    def test_password_verification(self):
        u = User(email='paws@his.house', password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    # tests from flasky
    def test_valid_confirmation_token(self):
        u = User(email='cookie@the.house.next.door',password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    '''
    def test_invalid_confirmation_token(self):
        u1 = User(password='cat')
        u2 = User(password='dog')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))
    '''
    '''
    def test_expired_confirmation_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        u.generate_confirmation_token()
        time.sleep(2)
        self.assertFalse(u.verify_password('cat'))
    '''

    def test_valid_reset_token(self):
        u = User(email='paws@his.house', password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        print( 'reset_token: ',token )
        self.assertTrue(User.reset_password(token, 'dog'))
        self.assertTrue(u.verify_password('dog'))

    '''
    def test_invalid_reset_token(self):
        u = User(email='cookie@next.door', password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertFalse(User.reset_password(token, 'horse'))
        self.assertTrue(u.verify_password('horse'))
    '''
    # confirm no longer returns a value
    '''
    def test_valid_timed_confirmation_token(self):
        u = User(email='paws@his.house',  password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        print('timed token: ',token)
        self.assertTrue(u.confirm(token) == 'paws@his.house')
        print('confirm_timed_token: ', u.confirm(token))
        self.assertFalse(u.confirm(token) == 'paws@my.house')

    def test_invalid_timed_confirmation_token(self):
        u1 = User(email='paws@his.house', password='cat')
        u2 = User(email='yapicrudi@horrible.house', password='dog')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(u1.email))

    def test_expired_timed_confirmation_token(self):
        u = User(email='tiny@bath', password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        time.sleep(2)
        self.assertFalse(u.confirm(token,1))
    '''
    
    #TODO
    '''
    def test_invalid_reset_token(self):
        u = User(email='cat@my.bed', password='cat')
        db.session.add(u)
        db.session.commit()
        reset = u.generate_reset_token('dog')
        print('reset_token', reset) # prints the encrypted token
        self.assertTrue(User.reset_password(reset, 'dog'))
        self.assertFalse(User.reset_password(reset, 'cat'))
        self.assertFalse(User.reset_password(reset, 'horse'))
    '''
        
    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.is_administrator())
        self.assertFalse(u.is_moderator())

    def test_timestamp(self):
        u = User( email='paws@his.house', password='cat')
        db.session.add(u)
        db.session.commit()
        self.assertTrue(
            (datetime.utcnow() - u.last_seen).total_seconds() < 3)

    # TODO
    '''
    def test_ping(self):
        u = User( email='paws@his.house', password='cat')
        db.session.add(u)
        db.session.commit()
        time.sleep(2)
        last_seen_before = u.last_seen
        u.ping()
        self.assertTrue(u.last_seen > last_seen_before)
    '''

    def test_is_administrator(self):
        u = User(email='john@example.com', password='cat')
        self.assertFalse( u.is_administrator() )
        u = User(email='jill@example.com', password='cat', is_admin=True)
        self.assertTrue( u.is_administrator() )
    
    def test_is_moderator(self):
        u = User(email='john@example.com', password='cat', is_mod=True)
        self.assertFalse( u.is_administrator() )
        self.assertTrue( u.is_moderator() )
        self.assertFalse( u.is_member )
        self.assertFalse( u.confirmed )

    def test_is_member(self):
        u = User(email='john@example.com', password='cat', is_member=True)
        self.assertFalse( u.is_administrator() )
        self.assertFalse( u.is_moderator() )
        self.assertTrue( u.is_member )
    
    def test_fullname(self):
        u = User(email='john@example.com', password='cat', first_name='Rosy', last_name='Lee')
        self.assertTrue( u.fullname() == 'Rosy Lee')

    '''
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