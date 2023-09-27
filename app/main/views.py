from datetime import datetime
from pathlib import Path
from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_required
from .forms import EditTopicForm, DeleteTopicForm, EditProfileForm, NewCommentForm, EditCommentForm, NewTopicForm, EmailForm, EditUserForm, DeleteUserForm, SetMeetingTimeForm, EditTopicFormDT
from .. import db
from ..models import Topic, User, Comment, MailList
#from ..decorators import admin_required, moderator_required
from . import main

# helper for index and topics
def get_topics():
  tl = { 'proposed_topics':[], 'future_topics':[], 'past_topics':[], 'online_topics':[] }
  topics = Topic.query.order_by(Topic.discussion_datetime).all()
  for topic in topics:
    tt = topic.dump()
    assert( isinstance(tt,dict))
    assert(tt['venue'] in ['proposed','online','planned','past'])
    tt['url'] = url_for('main.topic', topic_id=topic.id )
    if tt['venue'] == 'proposed':
        tl['proposed_topics'].append(tt)
    elif tt['venue'] == 'online':
        tl['online_topics'].append(tt)
    elif tt['venue'] == 'planned':
        tl['future_topics'].append(tt)
    elif tt['venue'] == 'past':
        tl['past_topics'].append(tt)
    else: 
        print('venue is:', tt['venue'])
        raise Exception("get_topics failed to find venue") 
    print(topic.discussion_datetime.strftime('%s'), tt['venue'] )
  return tl


@main.route('/')
def index():
    return render_template('index.html', tt_list=get_topics() )


#######################################################################################################
# All logged in users
#######################################################################################################

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = User.query.get(current_user.id)
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.continu.data:
            return redirect(url_for('.index'))
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        db.session.add(user)
        db.session.commit()
        flash(category='Info', message='Your profile has been updated to {}.'.format(user.fullname()))
        return redirect(url_for('main.edit_profile'))
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    return render_template('edit_profile.html', form=form)

@main.route('/newtopic', methods=['GET', 'POST'])
@login_required
def newtopic():
    if not current_user.is_member:
        return render_template('403.html')
    form=NewTopicForm()
    if request.method == 'POST' and form.validate():
        topic=Topic(title=form.title.data, summary=form.summary.data, author_id=current_user.id, author_fullname=current_user.fullname(), published=False)
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('newtopic.html',form=form)


# The user is allowed to choose between 'Online or proposed' venues
# An online venue has topic.published == False and topic.discussion date == datetime.max
# A proposed venue has topic.published == True and topic.discussion date == datetime.min
@main.route('/edittopic/<int:id>', methods=['GET','POST'])
@login_required
def edittopic(id):
    if not current_user.has_valid_profile() and not current_user.is_administrator():
        flash(category='Danger', message='You must complete your profile (so we can see who is proposing a new topic)')
        return redirect( url_for('main.edit_profile'))
    topic=Topic.query.get_or_404(id)
    if topic.discussion_venue() in ['proposed','online']:
        assert( topic.discussion_venue() in ['proposed','online'])
        form=EditTopicForm(topic=topic)
        if request.method == 'POST' and form.validate():
            topic.title=form.title.data
            topic.summary=form.summary.data
            topic.content=form.content.data
            topic.discussion_datetime=datetime.min
            topic.published=int(form.published.data)    # requires a boolean value
            if topic.published:
                topic.discussion_datetime=datetime.max
            print("topic.published set to {} ([(0,'Online Only'), (1,'Propose')])".format(topic.published))
            db.session.add(topic)
            db.session.commit()
            return redirect(url_for('.index'))
    elif topic.discussion_venue == 'planned':
        assert( topic.discussion_venue() in ['planned','past'])
        form=EditTopicFormDT(topic=topic) # A form with 'datetime' and without 'published'
    form.title.data=topic.title
    form.summary.data=topic.summary
    form.content.data=topic.content
    form.published.data = topic.published
    return render_template('edittopic.html',form=form)

'''
# if the event is past the topic.published may not be changed, so this is only used by planned topics
@main.route('/editplannedtopic/<int:id>', methods=['GET','POST'])
@login_required
def editplannedtopicdt(id):
'''


@main.route('/deletetopic/<int:id>', methods=['GET','POST'])
@login_required
def deletetopic(id):
    if not current_user.is_administrator:
        flash( category='Danger', message='Only an Administrator Can Delete a Topic!')

        return redirect( url_for('main.topics'))
    
    topic=Topic.query.get_or_404(id)
    form = DeleteTopicForm(topic=topic)
    if request.method == 'POST' and form.validate():
        comments=Comment.query.filter_by(topic_id = topic.id)
        for comment in comments:
            db.session.delete(comment)
        db.session.delete(topic) 
        db.session.commit()
        flash( category='Info', message='topic and all its comments deleted')
        return redirect(url_for('.topics'))
    print('Summary: {}'.format(topic.summary))
    form.summary.data=topic.summary
    form.title.data=topic.title
    return render_template('delete_topic.html',form=form)


@main.route('/topic/<int:topic_id>', methods=['GET'])
def topic(topic_id):
    try:
        user_id = current_user.id
    except:
        user_id = 0
    topic=Topic.query.get_or_404(topic_id)
    comments=Comment.query.filter_by(topic_id = topic.id)
    if topic.content == None:
        topic.content = "Waiting for content"
    return render_template('topic.html', topic=topic, comments=comments, user_id=user_id )


@main.route('/newcomment/<int:topic_id>', methods=['GET','POST'])
@login_required
def newcomment(topic_id):
    if not current_user.has_valid_profile():
        flash(category='Danger', message='You must complete your profile (so we can see who is commenting)')
        return redirect( url_for('main.edit_profile'))

    topic=Topic.query.get_or_404(topic_id)
    comment = Comment( topic_id=topic.id, author_id=current_user.id, author_fullname=current_user.fullname() )
    form = NewCommentForm(comment=comment)
    if request.method == 'POST' and form.validate():
        comment.content = form.content.data
        comment.author_id = current_user.id
        comment.author_fullname = current_user.fullname()
        comment.creation_datetime = datetime.now()
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('.topic', topic_id=topic_id))
    return render_template('newcomment.html', form=form, topic=topic )


@main.route('/editcomment/<int:comment_id>', methods=['GET','POST'])
@login_required
def editcomment( comment_id ):
    comment = Comment.query.get_or_404(comment_id)
    topic=Topic.query.get_or_404(comment.topic_id)
    form = EditCommentForm(comment=comment)
    if request.method == 'POST' and form.validate():
        comment.content = form.content.data
        if comment.content == "":
            db.session.delete(comment)
        else:
            db.session.add(comment)
        db.session.commit()
        return redirect(url_for('.topic', topic_id=comment.topic_id))
    form.content.data=comment.content
    return render_template('editcomment.html', form=form, topic=topic )


################################ Moderator or Administrator #######################################################

@main.route('/setmeetingtime/<int:topic_id>', methods=['GET','POST'])
@login_required
#@moderator_required
def setmeetingtime(topic_id):
    topic = Topic.query.filter_by(id=topic_id).first()
    form = SetMeetingTimeForm( topic_id=topic_id )
    if request.method == 'POST' and form.validate():
        topic.discussion_datetime=datetime.combine(form.discussion_date.data, form.discussion_time.data)
        db.session.add(topic)
        db.session.commit()
        return redirect( url_for('main.topics'))
    form.discussion_datetime = topic.discussion_datetime
    return render_template('setmeetingtime.html', form=form)


@main.route('/mailaddresses', methods=['GET','POST'])
@login_required
#@moderator_required
def mailaddresses():
    addresses = MailList.query.order_by('email').all()
    return render_template("mailaddresses.html", addresses=addresses)


####################################### Administrator Ony ##############################################################

@main.route('/users', methods=['GET', 'POST'])
@login_required
#@moderator_required
def users():
    users = User.query.order_by(User.email).filter(User.id>1).all()
    return render_template("users.html", users=users)


@main.route('/admin_edit-user/<int:id>', methods=['GET','POST'])
@login_required
#@admin_required
def edit_user(id):
    user=User.query.get_or_404(id)
    choices=Role.query.all()
    print("choices: ",choices)
    form = EditUserForm(user=user)
    form.choices=choices
    if request.method == 'POST' and form.validate():
        user.email = form.email.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.filter_by(name=form.role.data).first()
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.users'))
    form.email.data=user.email
    form.confirmed.data=user.confirmed
    return render_template('admin_edit_user.html', form=form )


@main.route('/delete-user/<int:id>', methods=['GET','POST'])
@login_required
#@admin_required
def delete_user(id):
    #if not current_user.is_administrator():
    #    return render_template('403.html')
    user=User.query.get_or_404(id)
    form = DeleteUserForm(user=user)
    if request.method == 'POST' and form.validate():
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('main.users'))
    return render_template('admin_delete_user.html', form=form )


@main.route('/add_email', methods=['GET','POST'])
@login_required
#@admin_required
def add_email():
    #if not current_user.is_administrator():
    #    return render_template('403.html')
    form=EmailForm()
    if request.method == 'POST' and form.validate():
        mli=MailList(email=form.email.data, datetime=datetime.now())
        db.session.add(mli)
        db.session.commit()
        return redirect(url_for('.mailaddresses'))
    return render_template('add_email.html',form=form)


@main.route('/edit_email/<int:id>', methods=['GET','POST'])
@login_required
#@admin_required
def edit_email(id):
    #if not current_user.is_administrator():
    #    return render_template('403.html')
    mail = MailList.query.get_or_404(id)
    #print("mail: {}".format(mail.email))
    form=EmailForm(mail=mail)
    if request.method == 'POST' and form.validate():
        mail.email = form.email.data
        mail.datetime=datetime.now()
        db.session.add(mail)
        db.session.commit()
        return redirect(url_for('.mailaddresses'))
    form.email.data=mail.email
    return render_template('edit_email.html',form=form)


@main.route('/delete_email/<int:id>', methods=['GET','POST'])
@login_required
#@admin_required
def delete_email(id):
    mail = MailList.query.get_or_404(id)
    db.session.delete(mail)
    db.session.commit()
    return redirect(url_for('.mailaddresses'))


