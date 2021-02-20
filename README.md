# weathercohn
Coding assignment for APAX job interview

Original challenge:

Build an interface that prompts a user’s location and displays the current weather info about the location. Integrate whichever weather source you feel comfortable integrating and explain why you selected that source.

The app should require a user to sign in (does not need to be a full authentication process, just ask for a username to track the user), and the user should be able to setup multiple locations to check weather. When the app updates the weather info, it should update each location. The users and their locations should be stored in a database.

This task can be solved in whichever language you prefer. Please use whichever language you feel best showcases your skills.

Commit the code to GitHub, BitBucket, or other hosted Git repository and share it with our team to review.

Summary:
I am a big lacrosse fan as a result of my son playing and coaching over the last 10 years so I sort of made this into a site a fan might go to and check weather for several different locations. Not a big factor in the design but it helped make it fun.

I built my solution using Flask and python because I had already been doing some work with Flask to expand my skills in a different web development framework. So I already had the basic environment running in a Ubuntu bash shell on my Windows10 desktop. I did a little research on weather api options for getting weather data and settled on openweathermap.org. I set up a free account and figured out how to access the data and decipher the json retun.

I used the SQLAlchemy library from flask to setup a very simple database in SQLite. I also had to install Flask shell to allow interacting with the SQLite database. The database also needed to be initialized with table definitions prior to use.  Flask and SQLAlchemy had some utilities to support this. 

The main toolbar has a site logo linked to default route, Login, Reload, Clear and Logout.

Login takes you to an empty login page which requires some sort of entry. It will result in a new entry in the database if the entered value does not match any names currently in the table.
Reload will display the weather page with the latest weather data for all saved locations for current user.
Clear will remove all saved locations for the current user.
Logout clears session data and returns to the login page.

The main weather display allows adding new locations by zip code and it will ignore duplicates. The input must be a number less than 99999.

