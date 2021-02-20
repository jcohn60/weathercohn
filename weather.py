import os
import sys
import json
import urllib.request
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import InputRequired
from wtforms.validators import NumberRange
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
#I am guessing this should be a little more cryptic
app.config['SECRET_KEY'] = 'Weather Is Always Good For Lacrosse'
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

#create the classes to define the data tables
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<User %r>' % self.username

class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    zip = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Zip %r>' %self.zip

#define the two forms used
class LoginForm(FlaskForm):
    uname = StringField('UserName ', validators=[InputRequired()])
    submit = SubmitField('Submit')

class NameForm(FlaskForm):
    #locale = IntegerField('Enter a Game Location By Zip: ')
    locale = IntegerField('Enter a Game Location By Zip: ', validators=[NumberRange(min=0, max=99999, message='Enter Valid Zip Code')])
    submit = SubmitField('Add')

#function to aid SQLalchemy database initialization
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, City=City)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
   return render_template('500.html'), 500

@app.route('/clear')
def clear():
    #delete this user's favorites
    City.query.filter_by(user_id=session['uid']).delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session['name'] = ''
    session['uid'] = ''
    return redirect(url_for('login'))

# Route for handling the login page logic
# for this exercise I am not doing any passowrd or user validation
# I just need uname to not be empty
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.uname.data =='':
        error = 'Invalid user Name. Please try again.'

    #Add new user if not already in the users table
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.uname.data).first()

        if user is None:
            new_user = User(username=form.uname.data)
            db.session.add(new_user)
            db.session.commit()

            #requery to get handle on new user to access id
            user = User.query.filter_by(username=form.uname.data).first()

        #set session variables for this user
        session['uid'] = user.id
        session['name'] = form.uname.data
        return redirect(url_for('index'))
    return render_template('login.html', form=form, error=error)

#route for the main weather display
@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    error = ''
    data = 'None'
    weather_list = []
    city_list = []

    #make sure we have a user to hit database
    if session['uid'] == '':
        return redirect(url_for('login'))

    #look for user location favorites in the database
    cityResult = City.query.filter_by(user_id=session['uid']).all()
    for db_city in cityResult:
        city_list.append(str(db_city.zip))

    #loop over cities and call function to get current weather for display
    for city in city_list:
        result = get_weather( city )
        if result != -1:
            weather_list.append( result )

    #Update database with new locations
    dupe = False
    if form.validate_on_submit():
        #loop over favorites and watch for duplication
        for city in city_list:
            if str(form.locale.data) == str(city):
                dupe = True
                error = 'Duplicate Zip Code. Please try again.'

        if not dupe:
            #insert into database using call to weather app to ensure we can get data for this zip
            result = get_weather( str(form.locale.data) )
            if result != -1:
                new_city = City(zip=form.locale.data, user_id=session['uid'])
                db.session.add(new_city)
                db.session.commit()
                return redirect(url_for('index'))
            else:
                error = 'Invalid Zip Code. Please try again.'

    return render_template('index.html', form=form, name=session.get('name'), weather=weather_list, ziperror=error)

#get weather in json format from my free account at openweathermap.org
#this site returns a 404 error if you send a zip code that is not valid
def get_weather( city ):
    api = '9e74cb4e236f9b0ffe42ab2e22d30d62'

    try:
        # source contains json data from api
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?zip=' + city + '&units=imperial&appid=' + api).read()

        #print(source)
        #sys.stdout.flush()

        # converting JSON data to a dictionary
        list_of_data = json.loads(source)

        # data for variable list_of_data to return
        data = {
            "city": str(list_of_data['name']),
            "temp": str(list_of_data['main']['temp']),
            "windchill": str(list_of_data['main']['feels_like']),
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
            "skies": str(list_of_data['weather'][0]['description']),
        }
        return data

    except urllib.request.HTTPError as exception:
        print(exception)
        sys.stdout.flush()
        return -1 
