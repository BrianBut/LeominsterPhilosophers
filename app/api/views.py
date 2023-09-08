from datetime import datetime, timedelta
import json
from flask import request, jsonify, url_for
from flask_login import current_user, login_required
from . import api
from .. import db
from ..models import Topic, User, Comment, MailList

'''
# used by views and index
@api.route('/sorted_topics/')
def get_topics():
  tl = { 'proposed_topics':[], 'future_topics':[], 'past_topics':[] }
  topics = Topic.query.order_by(Topic.discussion_datetime).all()
  for topic in topics:
    tt = topic.dump()
    tt['url'] = url_for('main.topic', topic_id=topic.id )
    if topic.discussion_datetime == datetime.min:
      tl['proposed_topics'].append(tt)
    elif topic.discussion_datetime > datetime.now():
      tl['future_topics'].append(tt)
    else:
      tl['past_topics'].append(tt)
  return jsonify( tl )


# not in use
@api.route('ping/<int:id>')
def ping(id):
  try:
    u = User.query.get_or_404(id)
    u.last_seen = datetime.utcnow()
    db.session.add(u)
    db.session.commit()
  except:
    return jsonify({"error": "user{} not found".format(id)}), 403 
  return jsonify( datetime.utcnow() )



@api.route('/topic/<int:id>')
def topic(id):
    t = Topic.query.get_or_404(id)
    return jsonify( {"id":t.id, "title":t.title, "discussion_datetime":t.discussion_datetime} )



# return the number of different users within the last five minutes
@api.route('/usercount/')
def members_present():
  users = User.query.all()
  present = []
  nows = datetime.now().timestamp()
  print("nows:",nows )
  for u in users:
      timediff = nows - u.last_seen.timestamp()
      print("username: {}      user: {},   timediff: {}".format(u.username, u.first_name, timediff))
      if timediff < 300:
        present.append("{} {}".format( u.first_name, u.last_name ))
  print("members_present: {}".format(present))
  return jsonify( {"count": len(present)} )

'''