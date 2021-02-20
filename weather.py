import os
import sys
import json
import urllib.request
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
#from wtforms.validators import NumberRange
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
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
    uname = StringField('UserName ', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NameForm(FlaskForm):
    locale = StringField('Where is today''s game (zip code) ? ', validators=[DataRequired()])
    submit = SubmitField('Submit')

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
    session['weather'] = ''
    #delete this user's favorites
    City.query.filter_by(user_id=session['uid']).delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session['name'] = ''
    session['uid'] = ''
    #session['locale'] = ''
    session['weather'] = ''
    return redirect(url_for('login'))

# Route for handling the login page logic
# for this exercise I am not doing any passowrd or user validation
# I just need uname to not be empty
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        if form.uname.data == '': 
            error = 'Invalid Credentials. Please try again.'
        else:
            # look for user in user table and add if not found
            user = User.query.filter_by(username=form.uname.data).first()

            if user is None:
                new_user = User(username=form.uname.data)
                db.session.add(new_user)
                db.session.commit()

                #requery to get handle on new object to access id
                user = User.query.filter_by(username=form.uname.data).first()

            session['uid'] = user.id
            session['name'] = form.uname.data
            return redirect(url_for('index'))
    return render_template('login.html', form=form, error=error)

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    data = 'None'
    weather_list = []
    city_list = []

    #make sure we have a user name to hit database
    if session['name'] == '':
        return redirect(url_for('login'))

    #look for user location favorites in the database
    cityResult = City.query.filter_by(user_id=session['uid']).all()
    for db_city in cityResult:
        print(db_city.zip)
        sys.stdout.flush()
        city_list.append(str(db_city.zip))

    for city in city_list:                    
        weather_list.append( get_weather( city ))

    session['weather'] = weather_list
    #print(weather_list) 
    #sys.stdout.flush()

    #if found make sure that session locale has their saved locations
    dupe = False

    if form.validate_on_submit():
        #loop over favorites and watch for duplication
        for city in city_list:
           print(city)
           sys.stdout.flush()
           if form.locale.data == city:
               dupe = True

        if not dupe:
            #insert into database 
            new_city = City(zip=form.locale.data, user_id=session['uid'])
            db.session.add(new_city)
            db.session.commit()

        return redirect(url_for('index'))

    return render_template('index.html', form=form, name=session.get('name'), weather=session.get('weather'))
    #return render_template('index.html', form=form, name=session.get('name'), locale=session.get('locale'), weather=session.get('weather'))

#get weather in json format from my free account at openweathermap.org
def get_weather( city ):
    api = '9e74cb4e236f9b0ffe42ab2e22d30d62'

    # source contain json data from api
    source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?zip=' + city + '&appid=' + api).read()

    # converting JSON data to a dictionary
    list_of_data = json.loads(source)

    # data for variable list_of_data
    data = {
        "city": str(list_of_data['name']),
        "coordinate": str(list_of_data['coord']['lon']) + ' '
                 + str(list_of_data['coord']['lat']),
        "temp": str(list_of_data['main']['temp']) + 'k',
        "pressure": str(list_of_data['main']['pressure']),
        "humidity": str(list_of_data['main']['humidity']),
    }

    return data
