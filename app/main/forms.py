from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, EmailField
from wtforms.fields import DateField, TimeField, SelectField
from wtforms.validators import DataRequired, Length

TOPIC_CHOICES = [(0,'Online Only'), (1,'Propose')]

class EditProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[Length(0, 32)])
    last_name = StringField('Last Name', validators=[Length(0, 32)])
    submit = SubmitField('Submit')
    continu = SubmitField('Continue')

# Form with discussion_venue
class NewTopicForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('About this topic')
    discussion_venue = SelectField( 'Topic Proposed or Online Only',choices=TOPIC_CHOICES)
    submit = SubmitField('Submit')

# Form which lacks a valid topic.datetime
class EditTopicForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('About This Topic')
    content = TextAreaField('Content (You can use Markdown here)') 
    published = SelectField( 'Topic Proposed or Online Only',choices=TOPIC_CHOICES)
    submit = SubmitField('Submit')

# Form which has a valid topic.datetime( User cannot set venue )
# As this form has a date and time field it cannot be used by a user - so how does a user with a planned topic edit?
class EditTopicFormDT(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('About This Topic')
    content = TextAreaField('Content (You can use Markdown here)') 
    discussion_date = DateField('Meeting Date')
    discussion_time = TimeField('Meeting Time')
    submit = SubmitField('Submit')

# User editing a planned topic
class EditPlannedTopicForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('About This Topic')
    content = TextAreaField('Content (You can use Markdown here)') 

class DeleteTopicForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('About This Topic')
    submit = SubmitField('Delete Topic and all comments about it')
    continu = SubmitField('Continue without deleting')

class NewCommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()]) 
    #published = BooleanField('Visible to all')
    submit = SubmitField('Submit')

class EditCommentForm(FlaskForm):
    content = TextAreaField('Content') 
    submit = SubmitField('Submit')

########################## Used by Moderator or Admin ###########################################
# TOGO
class SetMeetingTimeForm(FlaskForm):
    options=['proposed', 'online', 'scheduled']
    discussion_date = DateField('Meeting Date')
    discussion_time = TimeField('Meeting Time')
    submit = SubmitField('Submit')


########################## Used by Admin Only ####################################################

class EditUserForm(FlaskForm):
    email = EmailField('Email')
    role = SelectField('Role', choices=['Guest','User','Moderator'])                           
    confirmed = BooleanField('confirmed')
    submit = SubmitField('Submit')
    reset_password = SubmitField('Reset Password')


class DeleteUserForm(FlaskForm):
    submit = submit = SubmitField('Delete')
    continu = SubmitField('Continue without Deleting')


class EmailForm(FlaskForm):
    email = EmailField('Email')
    submit = SubmitField('Submit')
