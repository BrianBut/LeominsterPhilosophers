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
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    moderator = db.Column(db.Boolean, nullable=False, default=False)
    member = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        #print( 'user.email: ',self.email)
        #print('LP_ADMIN: ',current_app.config['LP_ADMIN'])
        if self.email == current_app.config['LP_ADMIN']:
            self.admin=True
            self.moderator=True
            self.member=True
        
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    # Next pair of functions generate confirmation tokens with timestamp
    def generate_confirmation_token(self):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(self.email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
    
    def confirm(self, token, expiration=3600):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = s.loads(
                token,
                salt=current_app.config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
            )
        except:
            return False
        if email != self.email:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    
    def generate_reset_token(self, expiration=3600):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'], expiration)
        return serializer.dumps({'id': self.id},salt=current_app.config['SECURITY_PASSWORD_SALT'])

    @staticmethod
    def reset_password(token, new_password, expiration=3600):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        print("token is: ",token)
        try:
            id = serializer.loads(
                token,
                salt=current_app.config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
                )
        except:
            return False
        
        print("id is:", id)
        user = User.query.get(id)
        print("user: ",user.id)
        if user.id is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def fullname(self):
        return "{} {}".format(self.first_name, self.last_name).strip()
    
    def is_member(self):
        return self.member
    
    def is_moderator(self):
        return self.moderator
    
    def is_administrator(self):
        return self.admin
    
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def __repr__(self):
        return f"<email {self.email}>"
    

class AnonymousUser(AnonymousUserMixin):

    def is_member(self):
        return False
    
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
