from flask_login import login_required, current_user
from werkzeug.utils import redirect
from app.view_models.trade import MyTrades
from app.models.base import db
from . import web
from app.models.gift import Gift
from flask import current_app, flash, url_for, render_template
from app.libs.enums import PendingStatus
from app.models.drift import Drift
__author__ = '七月'


@web.route('/my/gifts')
@login_required
def my_gifts():
    UID = current_user.id
    gifts_of_mine = Gift.get_user_gifts(UID)
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_counts(isbn_list)
    view_model = MyTrades(gifts_of_mine, wish_count_list)
    return render_template('my_gifts.html', gifts=view_model.trades)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            # database transaction
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
    else:
        flash('already added into gift or wish')
    return redirect(url_for('web.book_detail', isbn=isbn))

@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.Waiting).first()
    if drift:
        flash('please complete all pending status for this gift, then cancel it.')
    else:
        with db.auto_commit():
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
            gift.delete()
    return redirect(url_for('web.my_gifts'))


