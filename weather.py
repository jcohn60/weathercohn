from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import sys
import json
import urllib.request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Weather Is Always Good For Lacrosse'

bootstrap = Bootstrap(app)
moment = Moment(app)

class LoginForm(FlaskForm):
    uname = StringField('UserName ', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NameForm(FlaskForm):
    locale = StringField('Where is today''s game (zip code) ? ', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
   return render_template('500.html'), 500


@app.route('/clear')
def clear():
    session['name'] = ''
    session['locale'] = ''
    session['weather'] = ''
    return redirect(url_for('index'))

# Route for handling the login page logic
# for this exercise I am not doing any passowrd or user validation
# I just need uname to not be empty
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    #if request.method == 'POST':
    if form.validate_on_submit():
        if form.uname.data == '': 
            error = 'Invalid Credentials. Please try again.'
        else:
            # look for user in user table and add if not found

            session['name'] = form.uname.data
            return redirect(url_for('index'))
    return render_template('login.html', form=form, error=error)

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    data = 'None'
    weather_list = []

    #make sure we have a user name to hit database
    if session['name'] == '':
        return redirect(url_for('login'))

    #look for user location favorites in the database

    #if found make sure that session locale has their saved locations

    if form.validate_on_submit():
        #session['name'] = form.name.data
        if session['locale'] == '':
           session['locale'] = form.locale.data
        else:
           #check to see if this entry is saved in the database for this user

           session['locale'] = session['locale'] + ',' + form.locale.data

        if session['locale'] != '':
           city_list = session['locale'].split(',')

           for city in city_list:                    
               weather_list.append( get_weather( city ))

           session['weather'] = weather_list
           #print(weather_list) 
           #sys.stdout.flush()


        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), locale=session.get('locale'), weather=session.get('weather'))

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

#def update_user( name )

#def update_locale ( city )

#def delete_locale ( user, city )
