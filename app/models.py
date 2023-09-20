from datetime import datetime

from flask_login import UserMixin, AnonymousUserMixin

from app import bcrypt, db, login_manager


class MailList(db.Model):
    __tablename__ = 'mailist'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_mod = db.Column(db.Boolean, nullable=False, default=False)
    is_member = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    first_name = db.Column(db.String(32), )
    last_name = db.Column(db.String(32))
    
    # TODO COMPLETE
    def __init__( self, email, password, is_admin=False, is_mod=False, is_member=False, is_confirmed=False, confirmed_on=None, first_name=None, last_name=None ):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.created_on = datetime.now()
        self.is_admin = is_admin
        self.is_mod = is_mod
        self.is_member = is_member
        self.is_confirmed = is_confirmed
        self.confirmed_on = confirmed_on
        self.first_name = first_name
        self.last_name = last_name

    def fullname(self):
        return "{} {}".format(self.first_name, self.last_name).strip()
    
    def is_moderator(self):
        return self.is_mod
    
    def is_administrator(self):
        return self.is_admin
    
    def ping(self):
        self.last_seen = datetime.utcnow
        db.session.add(self)

    def __repr__(self):
        return f"<email {self.email}>"
    

class AnonymousUser(AnonymousUserMixin):
    
    def is_moderator(self):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    

class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    summary = db.Column(db.Text)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer)
    author_fullname = db.Column(db.String(64), default='Anon')
    creation_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    discussion_datetime = db.Column(db.DateTime, default=datetime.min)
    published = db.Column(db.Boolean, default=False)

    def discussion_date(self):
        if self.discussion_datetime == datetime.min:
            return "undecided"
        if self.discussion_datetime == datetime.max:
            return "never"
        return self.discussion_datetime.strftime('%a %d %b %Y')

    def discussion_time(self):
        if self.discussion_datetime:
            return self.discussion_datetime.strftime('%I:%M%p')
        return ""
    
    def discussion_venue(self):
        if self.discussion_datetime == datetime.min:
            return 'online'
        if self.discussion_datetime == datetime.max:
            return 'proposed'
        if self.discussion_datetime > datetime.now():
            return 'planned'
        return 'past'
    
    def dump(self):
        return { "id":self.id, "title":self.title, "summary":self.summary, "content":self.content, "published":self.published, "venue":self.discussion_venue(),
            "discussion_date":self.discussion_date(), "discussion_time":self.discussion_time(),  "author_id":self.author_id, "author_fullname":self.author_fullname }


class Comment(db.Model):
    __tablename__= 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    topic_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer)
    author_fullname = db.Column(db.String(64))
    creation_datetime = db.Column(db.DateTime, default=datetime.utcnow)
