from functools import wraps
from flask import abort, request, redirect, url_for
from flask_login import current_user
    
#from .models import Permission
# permission in [contribute, moderate, administrate]

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required('administrate')(f)

def moderator_required(f):
    return permission_required('moderate')(f)

def member_required(f):
    return permission_required('participate')


def member_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user is None:
            return redirect(url_for('login', next=request.url))
        if not current_user.is_member:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function