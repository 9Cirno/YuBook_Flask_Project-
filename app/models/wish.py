from app.models.base import db, Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, func, desc
from sqlalchemy.orm import relationship

from app.spider.YuShuBook import YuShuBook


class Wish(Base):
    id = Column(Integer, primary_key=True)
    launched = Column(Boolean, default=False)
    user = relationship('User')
    isbn = Column(String(15), nullable=False)
    uid = Column(Integer, ForeignKey('user.id'))

    # find gifts by uid
    @classmethod
    def get_user_wishess(cls, uid):
        wishes = Wish.query.filter_by(uid = uid, launched=False).order_by(
            desc(Wish.create_time)).all()
        return wishes

    @classmethod
    # filter needs conditions ==
    def get_gift_counts(cls, isbn_list):
        from app.models.gift import Gift
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(Gift.launched == False,
                                      Gift.isbn.in_(isbn_list),
                                      Gift.status == 1).group_by(
                                      Gift.isbn).all()
        count_dict = [{'count':w[0], 'isbn':[1]} for w in count_list]
        return count_dict

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first


#from app.models.gift import Gift
