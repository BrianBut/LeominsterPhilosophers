from datetime import datetime
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app, request, url_for
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
    password_hash = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_mod = db.Column(db.Boolean, nullable=False, default=False)
    is_member = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    first_name = db.Column(db.String(32), )
    last_name = db.Column(db.String(32))
    
    # TODO COMPLETE
    def __init__( self, email, password, is_admin=False, is_mod=False, is_member=False, is_confirmed=False, confirmed_on=None, first_name=None, last_name=None ):
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password)
        self.created_on = datetime.now()
        self.is_admin = is_admin
        self.is_mod = is_mod
        self.is_member = is_member
        self.confirmed = is_confirmed
        self.confirmed_on = confirmed_on
        self.first_name = first_name
        self.last_name = last_name

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    # Next pair of functions generate confirmation tokens with timestamp
    def generate_confirmation_token(self, email):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

    #def confirm_timed_token(self, token, expiration=3600):
    def confirm(self, token, expiration=3600):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt=current_app.config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
            )
        except:
            return False
        return email
    
    # Fails change password 
    def generate_reset_token(self, expiration=3600):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'], expiration)
        return serializer.dumps({'reset': self.id},salt=current_app.config['SECURITY_PASSWORD_SALT'])

    @staticmethod
    def reset_password(token, new_password, expiration=3600):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            id = s.loads(
                token,
                salt=current_app.config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
                )
        except:
            print("'reset_password' data not loaded")
            return False
        print("token is: ",id)
        user = User.query.get('token')
        print("id is:", user.id)
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True
    
    #From flasky
    #@staticmethod
    #def reset_password(token, new_password):
    '''
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True
    '''

    def fullname(self):
        return "{} {}".format(self.first_name, self.last_name).strip()
    
    def is_moderator(self):
        return self.is_mod
    
    def is_administrator(self):
        return self.is_admin
    
    def ping(self):
        self.last_seen = datetime.utcnow()
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
