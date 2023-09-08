from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask import current_app, request, url_for, flash
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime
from . import db, login_manager


# This is a list of persons who may be allowed to write or comment.
# Its datetime is the time it was created or modified
class MailList(db.Model):
    __tablename__ = 'mailist'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)


class Permission:
    READ = 1
    WRITE = 2
    MODERATE = 4
    ADMIN = 8


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'Guest': [Permission.READ],
            'User': [Permission.READ, Permission.WRITE],
            'Moderator': [Permission.READ, Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.READ, Permission.WRITE, Permission.MODERATE, Permission.ADMIN],
        }
        default_role = 'Guest'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions & perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:   # first login
            if self.email == current_app.config['LP_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    #def generate_confirmation_token(self, expiration=3600):
    #    s = Serializer(current_app.config['SECRET_KEY'], str(expiration))
    #    return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        self.role.add_permission(Permission.WRITE)
        db.session.add(self)
        return True

    #def generate_reset_token(self, expiration=3600):
    #    s = Serializer(current_app.config['SECRET_KEY'], str(expiration))
    #    return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
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
    
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], str(expiration))
        return s.dumps({'confirm': self.id})
    
    def generate_reset_token(self, expires_sec=3600):
        s = Serializer(current_app.config['SECRET_KEY'], str(expires_sec))
        return s.dumps({'reset': self.id}) 

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True
    
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
    
    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen
        }
        return json_user
    
    def can(self, perm):
        #return self.role is not None and self.role.has_permission(perm)
        return self.role.has_permission(perm)

    # a profile is valid if contains at least 3 characters in its full_name
    def has_valid_profile(self):
        if self.first_name and self.last_name and len(self.fullname()) > 3:
            return True
    
    # A user will not have an id unless he or she has registered
    def is_guest(self):
        if hasattr(self, 'id'):
            return True
    
    def is_moderator(self):
        return self.can(Permission.MODERATE)

    def is_administrator(self):
        return self.can(Permission.ADMIN)
    
    def is_on_mailing_list(self):
        if MailList.query.filter_by(email=self.email).first() is not None:
            return True
        
    def fullname(self):
        return "{} {}".format(self.first_name, self.last_name).strip()
    
    @staticmethod
    def insert_admin(uname, pwd):
        role_id = Role.query.filter_by(name='Administrator').first()
        user = User(email=current_app.config['LP_ADMIN'], password=pwd, username=uname, role_id=role_id, confirmed=True)
        db.session.add(user)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
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
        return self.discussion_datetime.strftime('%a %d %b %Y')

    def discussion_time(self):  
        return self.discussion_datetime.strftime('%I:%M%p')
    
    def venue(self):
        if ( self.discussion_datetime - datetime.now() ).total_seconds() > 0:
            return 'planned'
        if ( self.discussion_datetime - datetime.min ).total_seconds() > 0:
            return 'past'
        if self.published:
            return 'proposed'
        return 'online'
       
    def dump(self):
        return { "id":self.id, "title":self.title, "summary":self.summary, "content":self.content, "published":self.published, "venue":self.venue(),
            "discussion_date":self.discussion_date(), "discussion_time":self.discussion_time(),  "author_id":self.author_id, "author_fullname":self.author_fullname }

# 27th August 'published' is not currently in use, but keep it rather than alter the database 
class Comment(db.Model):
    __tablename__= 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    topic_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer)
    author_fullname = db.Column(db.String(64))
    creation_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    published = db.Column(db.Boolean, default=True)
