import unittest
import time
from datetime import datetime
from app import create_app, db
from app.models import Role, Permission, User, AnonymousUser


class RoleModelTestCase(unittest.TestCase):
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
    
    '''
    def test_administrator_role(self):
        r = Role.query.filter_by(name='Administrator').first()
        u = User(email='john@example.com', password='cat', role=r)
        self.assertTrue(u.can(Permission.READ))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertTrue(u.can(Permission.MODERATE))
        self.assertTrue(u.can(Permission.ADMIN))
    '''
    
    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.READ))
        self.assertFalse(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))
    '''
    def test_guest_role(self):
        r = Role.query.filter_by(name='Guest').first()
        u = User(email='john@example.com', password='cat', role=r)
        self.assertTrue(u.can(Permission.READ))
        self.assertFalse(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))
    '''
    '''
    def test_user_role(self):
        r = Role.query.filter_by(name='User').first()
        u = User(email='john@example.com', password='cat', role=r)
        self.assertTrue(u.can(Permission.READ))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))
    '''