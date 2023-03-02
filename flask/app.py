from flask import Flask, render_template, url_for, request, session, redirect, send_from_directory
import datetime

app = Flask(__name__)
app.secret_key = '??^W.;? '


@app.route('/hello/<name>')
def helloName(name=None):
    page = request.path
    session['visits'][page] = session['visits'].get(page, 0) + 1
    now = datetime.datetime.now()
    if now.hour < 12:
        message = "Good morning!"
    elif now.hour < 18:
        message = "Good afternoon!"
    else:
        message = "Good evening!"
    return (render_template('hi.html', message=message, name=name))


@app.route('/')
def index():
    return send_from_directory('static/html', 'index.html')


@app.route('/fatPets/<whichPet>')
def showPets(whichPet):
    page = request.path
    session['visits'][page] = session['visits'].get(page, 0) + 1
    image_url = url_for('static', filename=whichPet+'.jpg')
    return render_template('pets.html', image_url=image_url)


@app.route('/logout')
def logout():
    # remove the 'logged_in' key from the session object
    session.pop('logged_in', None)
    return redirect(url_for('login'))


users = {
    'rachel': 'password123',
    'admin': 'admin',
}


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['logged_in'] = True
            session['username'] = username
            if 'visits' not in session:
                session['visits'] = {}
            page = request.path
            session['visits'][page] = session['visits'].get(page, 0) + 1
            return redirect(url_for('secret'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')


@app.route('/secret')
def secret():
    page = request.path
    session['visits'][page] = session['visits'].get(page, 0) + 1
    if 'logged_in' in session and session['logged_in']:
        return 'This is a secret page! My eyes only!'
    else:
        return redirect(url_for('login'))


@app.route('/visits')
def visits():
    # Check if the user is logged in
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Display the visit counts for each page
    visits = session.get('visits', {})
    return render_template('visits.html', visits=visits)
