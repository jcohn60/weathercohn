from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Weather Is Always Good For Lacrosse'

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('What is your name? ', validators=[DataRequired()])
    locale = StringField('Where do you want to play? ', validators=[DataRequired()])
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
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        if session['locale'] != '':
           session['locale'] = session['locale'] + ', ' + form.locale.data
        else:
           session['locale'] = form.locale.data

        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), locale=session.get('locale'))
