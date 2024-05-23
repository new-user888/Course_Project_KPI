from flask import render_template, redirect, url_for
from app.auth.forms import RegistrationForm, LoginForm
from app.auth import auth
from app.auth.models import User
from flask_login import login_user, logout_user, login_required, current_user


@auth.route('/login', methods=['GET', 'POST'])
def login_user_session():

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(user_name=login_form.name.data).first()
        if not user or not user.check_password(login_form.password.data):
            return render_template('login_failed.html')

        login_user(user, login_form.stay_logged_in.data)
        return redirect(url_for('main.main_page'))
    return render_template('login_page.html', form=login_form)


@auth.route('/logout')
@login_required
def logout_user_session():
    logout_user()
    return redirect(url_for('main.main_page'))


@auth.route('/register', methods=['GET', 'POST'])
def register_user():
    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        User.create_user(
            user=reg_form.name.data,
            bio=reg_form.about.data,
            private=reg_form.private.data,
            password=reg_form.password.data
        )
        return redirect(url_for('authentication.reg_success'))

    return render_template('register_page.html', form=reg_form)


@auth.route('/reg_successfull')
def reg_success():
    return render_template('reg_successfull.html')

