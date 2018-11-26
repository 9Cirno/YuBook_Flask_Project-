from . import web
from app.models.base import db
from app.models.user import User
from flask import render_template, request, redirect, url_for, flash
from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from flask_login import login_user,logout_user
from app.libs.email import send_mail
__author__ = '七月'


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form = form)



@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user) # ,remember = True
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('account not exist or password is wrong')
        pass
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':

        if form.validate():
            account_email = form.email.data
            user = User.query.filter_by(email=account_email).first_or_404()
            send_mail(form.email.data, 'reset your password','email/reset_password.html',
                      form=form,user=user,token=user.generate_token())
            flash('a email sent to your address, please check and follow instruction to change password')
            #return redirect(url_for('web.login'))
    return render_template('auth/forget_password_request.html')


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token, form.password1)
        if success:
            flash('reset password successfully')
            return redirect(url_for('web.login'))
        else:
            flash('reset password failed')
    return render_template('auth/forget_password.html', form=form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
