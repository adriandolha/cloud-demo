import logging

from authlib.jose import jwt
from flask import Blueprint, flash, url_for, request, jsonify, current_app, make_response
from flask import render_template, redirect
from flask_login import login_user, login_required, logout_user, current_user

from website.routes import app_context
from . import login_manager, db
from .forms import LoginForm, RegistrationForm
from .models import User, LoginType

auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)
LOGGER = logging.getLogger('lorem-ipsum')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.request_loader
def load_user_from_request(request):
    auth_headers = request.headers.get('Authorization', '').split()
    if len(auth_headers) != 2:
        return None
    try:
        token = auth_headers[1]
        data = jwt.decode(token, current_app.config['SECRET_KEY'])
        user = User.by_email(data['sub'])
        if user:
            return user
    except jwt.ExpiredSignatureError:
        return None
    except (jwt.InvalidTokenError, Exception) as e:
        return None
    return None


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_basic_user(email=form.email.data)
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/health', methods=['GET'])
def health():
    LOGGER.info('Checking system health...')
    return 'all_good'


@login_manager.request_loader
def load_user_from_request(request):
    _app_context = app_context()
    auth_headers = request.headers.get('Authorization', '').split()
    if len(auth_headers) != 2:
        return None
    try:
        token = auth_headers[1]

        data = _app_context.user_service.decode_auth_token(token)
        user = User.by_email(data['sub'])
        if user:
            return user
    except jwt.ExpiredSignatureError:
        return None
    except (jwt.InvalidTokenError, Exception) as e:
        return None
    return None


@auth.route('/api/me', methods=['GET'])
@login_required
def me():
    user = current_user
    return jsonify(id=user.id, username=user.username)
