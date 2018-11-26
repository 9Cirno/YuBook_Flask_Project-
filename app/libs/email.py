# pip install flask-mail
from threading import Thread
from app import mail
from flask_mail import Message
from flask import current_app, render_template


# need to push current_app into stack
# direct pass current_app will not work since the proxy app sent
# current_app._get_current_object() will pass the instance


def send_async_email(current_app, msg):
    with current_app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_mail(to, subject, template, **kwargs):
    # to, subject, template
#
    msg = Message('[鱼书]'+' ' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    thr = Thread(target=send_async_email, args=[current_app._get_current_object(), msg])
    thr.start()
