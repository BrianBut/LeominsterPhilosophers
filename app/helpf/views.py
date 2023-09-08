from flask import render_template, redirect, request, url_for, flash
from . import helpf

@helpf.route('getting_started')
def getting_started():
  mkd='''###Getting Started

1.  Before you can participate in the online discussion you must register and login.</li>

2.  Your registration must be approved before you can log in. Hopefully everyone who is on the mailing list for the Leominster Philosophy Group will already be approved.</li>

3.  If you are already a member of the group, and you find your registration not approved contact Brian or John Hoskinson</li>

4.  If you are not yet a member of the group, and you would like to be registered please email Phil Leominster, <A HREF="mailto:phil_leominster@proton.me">phil_leominster@proton.me</A> or ?</li> You might have to wait for the reply for a couple of days
    depending on how often we read our email.
'''
  return render_template('helpf.html',mkd=mkd)


@helpf.route('code_of_conduct')
def code_of_conduct():
  mkd='''###Code of Conduct  

1. The object of this website/app is to initiate and develop philosophical discussions. Often when we listen to a talk or discussion, 
questions or comments arise a few days later. This website is designed to let you put and develop those questions or comments. 

2. We welcome questions and developed and well explained opinions. You should provide reasons for any opinions you express. The more fully developed, the better.

3. We do not welcome short opinions without reasons nor abuse in any form. A simple statement of the form 'I agree', could be acceptable in response to a clearly stated 
argument, but 'I disagree' without reason would not, as it lacks reason or reasons.

'''
  return render_template('helpf.html',mkd=mkd)



@helpf.route('register_and_login')
def register_and_login():
  mkd='''###Register and Login  
    
Before you can participate in the online discussion you must register and login.  
  
Your registration must be approved before you can log in. Hopefully everyone who is on the mailing list for the Leominster Philosophy Group will already be approved.  
  
If you are already a member of the group, and you find your registration not approved contact Brian or John Hoskinson.  
  
If you are not yet a member of the group, and you would like to be registered please email '<phil_leominster@proton.me>'. 
  You might have to wait for the reply for a couple of days depending on how often we read our email.  

#### How our registration works  
  
The site maintains a list of approved email addresses which can be used for registration. Initially this is the group's mailing list (I hope). The the site administrator or moderators can
add or remove names as required. Registrations are only accepted from addresses which are on that list.
If you register online, and your email address is not accepted, this will be because we do not know you, or we have made a mistake. Please contact us.  

#### Full Name or 'nom de plume'  

You need to provide you full name or preferred name before you can write comments or topics for discussion.  

'''
  return render_template('helpf.html',mkd=mkd)


@helpf.route('scheduling')
def scheduling():
  mkd='''##The Moderator and Scheduling
  
  Only users with moderator privileges can select and schedule topics for discussion at meetings. At the moment there are no plans to grant moderator privileges to any user other than John H.

  When a logged in moderator looks at the detail on the topics page he sees an orange button labelled, 'Set Time'. This enables him to set the date and time for a meeting.

  The moderator can delete unsuitable comments, correct spelling or make any other changes to entries which other users have made.
  
  The orange colour is a warning to the moderator that he can alter the database in ways which might not be desired.
'''
  return render_template('helpf.html',mkd=mkd)


@helpf.route('writing_markdown')
def writing_markdown():
  mkd='''##Writing Markdown

Text boxes for topic summaries, topic content and comments on this website can be formatted in markdown to produce a nicely formatted page.  
Markdown is said to be very simple but I have found it tricky to get used to.
##Getting Started with markdown

see: [Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/):

I have also found this url usefull:(<https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax>)
  
I used to have an easier cheetsheet, but it no longer seems to be online. When it does surface I will add the link to this page.
'''
  return render_template('helpf.html',mkd=mkd)

@helpf.route('table_topics')
def table_topics():
  mkd='''Table Topics
  `class Topic(db.Model):
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
`
'''

