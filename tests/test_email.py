import os
import unittest
from datetime import datetime, time
from app import create_app, db
from flask_mail import Message
#from flask_mail import mail

#from app.models import User, AnonymousUser, Role, Permission, Topic
MAIL_DEFAULT_SENDER = 'leominsterphil@proton.me'


class EmailModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_message_sender_default(self):
        sender = MAIL_DEFAULT_SENDER
        #print("sender: {}".format(sender))
        self.assertFalse(sender == None)

    def test_message_sender(self):
        msg = Message("Hello", sender=MAIL_DEFAULT_SENDER, recipients=["to@example.com"])
        #print("sender: {}".format(msg.sender))
        self.assertTrue(msg.sender == MAIL_DEFAULT_SENDER)

    
    def test_message_recipient(self):
        msg = Message("Hello", sender=MAIL_DEFAULT_SENDER, recipients=["to@example.com"])
        #print("recipients: {}".format(msg.recipients))
        self.assertTrue(msg.recipients[0] == "to@example.com")
