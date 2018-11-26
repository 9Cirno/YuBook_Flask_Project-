from app.models.base import db, Base
from sqlalchemy import Column, Integer, func, String, Boolean, Float,ForeignKey,desc,SmallInteger
from sqlalchemy.orm import relationship
from math import floor
from app.libs.enums import PendingStatus
class Drift(Base):
    id = Column(Integer, primary_key = True)

    # shipment info
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)

    # request info
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(80))
    book_img = Column(String(50))

    # sender info
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    # gifter info
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))

    _pending = Column('pending', SmallInteger, default=1)

    # request_id = Column(integer, Fore
    # ignKey('user.id'))
    # requester = relationship('User')
    # gift_id = Column(Integer, ForeignKey('gift.id))
    # gift = relationship('Gift')

    @property
    def pending(self):
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        self._pending = status.value
