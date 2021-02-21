# weathercohn
Coding assignment for APAX job interview

**
Original challenge:

Build an interface that prompts a user’s location and displays the current weather info about the location. Integrate whichever weather source you feel comfortable integrating and explain why you selected that source.

The app should require a user to sign in (does not need to be a full authentication process, just ask for a username to track the user), and the user should be able to setup multiple locations to check weather. When the app updates the weather info, it should update each location. The users and their locations should be stored in a database.

This task can be solved in whichever language you prefer. Please use whichever language you feel best showcases your skills.

Commit the code to GitHub, BitBucket, or other hosted Git repository and share it with our team to review.
**

Summary:
I am a big lacrosse fan as a result of my son playing and coaching over the last 10 years so I sort of made this into a site a fan might go to and check weather for several different locations. Not a big factor in the design but it helped make it fun.

I built my solution using Flask and python because I had already been doing some work with Flask to expand my skills in a different web development framework. So I already had the basic environment running in a Ubuntu bash shell on my Windows10 desktop.

Below is the ouput from pip freeze which shows all installed packages in my flask environment;

click==7.1.2
dominate==2.6.0
Flask==1.1.2
Flask-Bootstrap==3.3.7.1
Flask-Moment==0.11.0
Flask-SQLAlchemy==2.4.4
Flask-WTF==0.14.3
itsdangerous==1.1.0
Jinja2==2.11.3
MarkupSafe==1.1.1
SQLAlchemy==1.3.23
visitor==0.1.3
Werkzeug==1.0.1
WTForms==2.3.3

I did a little research on weather api options for getting weather data and settled on openweathermap.org. I set up a free account and figured out how to access the data and decipher the json return. The API requires a key from your openweathermap accounti. This key should be exported to WEATHER_KEY in the environment where flask is running.

I used the SQLAlchemy library from flask to setup a very simple database in SQLite. I also installed Flask shell to allow interacting with the SQLite database from a command line. The database also needed to be initialized with table definitions prior to use.  Flask and SQLAlchemy had some utilities to support this. To init the database I ran the following while logged in to flask shell:

from weather.py import db

db.create_all()

I was reading the documentation for SQLAlchemy and it does provide some built in features that provide security against some web attack methods such as sql injection. I feel like I would have some more work to do to harden the interface against other types of attacks which will require more research and learning on my part.

The templates are developed using Jinja2.

The main toolbar has a site logo linked to default route, Login, Reload, Clear and Logout.

Login takes you to an empty login page which requires some sort of entry. It will result in a new entry in the database if the entered value does not match any names currently in the table. The only validation I have is against empty string.

Reload will display the weather page with the latest weather data for all saved locations for current user.

Clear will remove all saved locations for the current user.

Logout clears session data and returns to the login page.

The main weather display allows adding new locations by zip code and it will ignore duplicates. The input must be a number less than 99999 that is a valid US zip code. Validating this was a challenge and I managed to develop a combination of things to make it work. The weather display is very basic, I was just trying to demonstrate the concept.

To Do's
Add a delete button for each weather location rather than the clear all function I have now.
If I was going farther with this I would definitely work to harden the application against attack.
I would also make the web pages more interesting visually.
