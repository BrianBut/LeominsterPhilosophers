import unittest
from datetime import datetime, time
from app import create_app, db
from app.models import User, AnonymousUser, Topic


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

    def test_title(self):
        t = Topic(title="Test Topic")
        self.assertTrue(t.title is not None)

    def test_creation_datetime(self):
        t = Topic(title="Test Topic")
        db.session.add(t)
        db.session.commit()
        t2 = Topic.query.first()
        print("t.creation_datetime: {}".format(t2.creation_datetime))
        self.assertTrue(t.creation_datetime is not None)

    def test_discussion_datetime(self):
        t = Topic(title="Test Topic")
        db.session.add(t)
        db.session.flush()
        print("t.discussion_datetime: {}".format(t.discussion_datetime))
        self.assertTrue(t.discussion_datetime == datetime.min)

    def test_discussion_timediff(self):
        t = Topic(title="Test Topic")
        db.session.add(t)
        db.session.flush()
        timediff_in_seconds = ( t.discussion_datetime - datetime.min ).total_seconds()
        print( 'timediff', timediff_in_seconds )
        assert isinstance(timediff_in_seconds, float)
        self.assertTrue(timediff_in_seconds < 0.5)

    def test_published_is_false(self):
        t = Topic(title="Test Topic")
        db.session.add(t)
        db.session.flush()
        self.assertTrue(t.published == False)

    def test_default_is_proposed(self):
        t = Topic(title="Test Topic")
        db.session.add(t)
        db.session.flush()
        db.session.commit()
        #t2 = Topic.query.first()
        #print(t.dump())
        self.assertTrue(t.discussion_venue() == 'online')
    '''
    
    
    def test_proposed_topic(self):
        t=Topic(title="Test Proposed Topic")
        db.session.add(t)
        db.session.commit()
        tlists = get_sorted_topics()
        print( tlists['proposed_topics'][0]['title'] )
        self.assertTrue(tlists['proposed_topics'][0]['title']=="Test Proposed Topic")

    def test_future_topic(self):
        t=Topic(title="Test Future Topic", discussion_datetime = datetime.max)
        db.session.add(t)
        db.session.commit()
        tlists=get_sorted_topics()
        self.assertTrue(tlists['future_topics'][0]['title']=="Test Future Topic")

    def test_past_topic(self):
        t=Topic(title="Test Past Topic", discussion_datetime = datetime.now())
        db.session.add(t)
        db.session.commit()
        tlists = get_sorted_topics()
        self.assertTrue(tlists['past_topics'][0]['title']=="Test Past Topic")
    '''
        
    def test_dump_topic(self):
        t=Topic(title="Test Proposed Topic")
        db.session.add(t)
        db.session.flush()
        topic = t.dump()
        #print( "dump: ", topic)
        self.assertTrue(topic["id"]==1)
        self.assertTrue(topic["title"]=="Test Proposed Topic")
        #print(topic["discussion_date"])
        self.assertTrue(topic["discussion_date"]== 'undecided')

    '''
    def test_topic_author_full_name(self):
        u = User(email='johnsmith@example.com', password='cat', first_name='Rosy', last_name='Lee')
        db.session.add(u)
        db.session.commit()
        t=Topic(title="Test Author Fullname", author_id=u.id, authorfullname=u.fullname())
        #print(t.author_fullname())
        self.assertTrue(t.authorfullname == 'Rosy Lee')
    '''