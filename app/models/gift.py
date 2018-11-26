from app.models.base import db, Base
from sqlalchemy import Column, Integer, func, String, Boolean, Float,ForeignKey,desc
from sqlalchemy.orm import relationship
from flask import current_app
from app.spider.YuShuBook import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)
    launched = Column(Boolean, default=False)
    user = relationship('User')
    isbn = Column(String(15), nullable=False)
    uid = Column(Integer, ForeignKey('user.id'))


    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

    # find gifts by uid
    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid = uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    # filter needs conditions ==
    def get_wish_counts(cls, isbn_list):
        from app.models.wish import Wish
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(Wish.launched == False,
                                      Wish.isbn.in_(isbn_list),
                                      Wish.status == 1).group_by(
                                      Wish.isbn).all()
        count_dict = [{'count':w[0], 'isbn':[1]} for w in count_list]
        return count_dict

    @classmethod
    def recent(self):
        recent_gift = Gift.query.filter_by(
            launched=False).group_by(
            Gift.isbn).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()

        return recent_gift

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

#from app.models.wish import Wish
