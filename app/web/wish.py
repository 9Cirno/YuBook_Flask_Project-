from . import web
from flask import render_template, flash,redirect,url_for
from flask_login import current_user, login_required
from app.models.wish import Wish
from app.view_models.trade import MyTrades
from app.models.base import db
from app.models.gift import Gift
from app.libs.email import send_mail
__author__ = '七月'


@web.route('/my/wish')
@login_required
def my_wish():
    uid = current_user.id
    wishes_of_mine = Wish.get_user_wishess(uid)
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    gift_count_list = Wish.get_gift_counts(isbn_list)
    view_model = MyTrades(wishes_of_mine, gift_count_list)
    return render_template('my_wish.html', wishes=view_model.trades)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.uid = current_user.id
            wish.isbn = isbn
            db.session.add(wish)
    else:
        flash("you already added this book in your wish list")
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
@login_required
def satisfy_wish(wid):
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(uid=current_user.id, isbn=wish.isbn).fist()
    if not gift:
        flash('you need added this book to gift list before send it to others~')
    else:
        send_mail(wish.user.email,'Someone Wants to Send You a Book','email/satisify_wish.html', wish=wish, gift=gift)
        flash("you have send a email to notify the receiver, if he or she accept your gift, you will receive a drift")
    return redirect('web.book_detail',isbn=wish.isbn)

@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    wish = Wish.query.filter_by(isbn=isbn, launched=False).first_or_404()
    with db.auto_commit():
        wish.delete()
    return redirect(url_for('web.my_wish'))
