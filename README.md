SquareExplo

Video Demo:  https://www.youtube.com/watch?v=zYc2O4QZR5g

Description:
    For CS50 Final Project I created an App with Flask with a simple game with
Javacript and HTML, connected with a Database.
    The app has a Tab for the user to register, to login and to log out.
The passwords are converted in an hash on the database, for security reasons.
    Once the user logs in, the user as a Game and can submit the scores, being
the scores added to the database. Additionally there is a small music Playlist
and the Best Scores Tab.
    In terms of design I adopted a simplist approach, because I like apps with
a simple clear look and not too many colors, styles and information, as I believe
makes easier for the user to find the information.

Templates description:
    Apology - The appology file trows back an error to the user, every time the user
provides wrong information or there is an issue with the server.
    History - On the History the template gets back using SQL the users with better
scores in each level and the users with best total scores.
    Index - The index template is the main tempate on the app, on this template the
user can find the instruction for the game, the game it self, finally can submit the
score. The code for the game is also included in this file and takes advantage of
canvas properties to with Javascript create the animations on the game.
    Layout - The layout as the name indicates, is the main template file used for the
structure in all the other templates, on the file the main design and link for the app
is found.
    Login - On this template the user can login, by adding the same user name and password,
that we registered on the registry page.
    Music - Here the user can find a small play list with 3 of my personal musics, the
user can choose to play, to change music, or to pause the musics.
    Register - On this final template the user can register a user name with a minimum
length of 4 characters and a password that will be stored as an hash once the user confirms
the password.

Final DB:
    This Database final.db this database was created for the user to be able to introduce
is username, password and to be able to submit the scores, is based on Sqlite and the
connection is seted in the application file.

Helpers:
    The helpers file is the same file provided previouly be CS50 for the finance project,
for this project it was keep the login and the apology. The login function allows was
added to the application file, to limit the access to the app only after the user login.

Application:
    On this file the structure of the app is defined with Python and, more specifically
Flask, a micro web framework written in Python. On this file is defined the connection
between the user, server and the database. Trowing back errors if the data is not found,
or doesn't match and retrieving or adding the data if the data is correct.
