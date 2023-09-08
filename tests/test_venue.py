import unittest
import datetime
from app import create_app, db
from app.models import Topic


class TopicModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_topic_default(self):
        t = Topic(title='test1')
        self.assertTrue( t.title == 'test1')
        print(t.discussion_datetime)
        #print(unixepoch( t.discussion_datetime)
        