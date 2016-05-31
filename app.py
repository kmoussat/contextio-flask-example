"""
    ContextIO Example Flask App
    ~~~~~~

    A Simple example of using the CIO Python client library in
    tandem with Flask

"""

import os
from flask import Flask, request, redirect, render_template, flash
from flask.ext.login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
import contextio as c

PORT = os.environ.get("PORT", 8080)
CONSUMER_KEY = os.environ.get("CIO_CONSUMER_KEY", "")
CONSUMER_SECRET = os.environ.get("CIO_CONSUMER_SECRET", "")

API_VERSION = '2.0'

# our fake db
users = {}

context_io = c.ContextIO(
  consumer_key=CONSUMER_KEY,
  consumer_secret=CONSUMER_SECRET,
  api_version=API_VERSION
)

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.config.update(dict(
    SECRET_KEY="1234",
    DEBUG=True
))

class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    user.first_name = users[email]["first_name"]
    user.last_name = users[email]["last_name"]
    return user


@login_manager.unauthorized_handler
def unauthorized_handler():
    flash({"type": "danger", "text": "Ah ah ah... you didn't say the magic word!", "dennis": 1})
    return redirect("/sign-in", code=302)

@app.route('/protected', methods=["GET"])
@login_required
def protected():
    return 'Logged in as: ' + current_user.id

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/sign-in', methods=["GET"])
def get_sign_in():
    return render_template('sign-in.html')

@app.route('/sign-in', methods=["POST"])
def post_sign_in():
    email = request.form.get('email', None)
    if users.get(email, None):
        if request.form['password'] == users[email]['pw']:
            user = User()
            user.id = email
            login_user(user)
            return redirect("/landing-page", code=302)

    flash({"type": "danger", "text": "Incorrect email or password", "dennis": 1})
    return redirect("/sign-in", code=302)

@app.route('/sign-up', methods=["GET"])
def get_sign_up():
    return render_template('sign-up.html')

@app.route('/sign-up', methods=["POST"])
def post_sign_up():
    email = request.form.get('email', None)
    if email is None:
        flash({"type": "danger", "text": "Ummm... you didn't enter an email"})
        return redirect("/sign-up", code=302)

    if email in users:
        flash({"type": "danger", "text": "'{0}' already exists".format(email)})
        return redirect("/sign-up", code=302)

    users[email] = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "pw": request.form["password"]
    }

    user = User()
    user.id = email
    login_user(user)

    connect_token_request = context_io.post_connect_token(
        first_name=request.form["first_name"],
        last_name=request.form["last_name"],
        email=email,
        callback_url="http://localhost:{0}/landing-page".format(PORT))
    return redirect(
        "{0}&skip_oauth_splash=1".format(connect_token_request["browser_redirect_url"]), code=302)


@app.route('/landing-page', methods=['GET'])
@login_required
def get_landing_page():
    account = context_io.get_accounts(email=current_user.id)[0]
    messages = account.get_messages(limit=5)

    return render_template(
        'landing-page.html', is_logged_in=True, user=current_user, messages=messages)

@app.route('/logout')
def logout():
    logout_user()
    flash({"type": "success", "text": "You have been logged out"})
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
