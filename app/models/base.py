from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from flask_sqlalchemy import BaseQuery
from sqlalchemy import Column, Integer, String, Boolean, Float,SmallInteger
from contextlib import contextmanager
from datetime import datetime


# rewrite the SQLAlchemy to enable the context for late use
class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


# rewrite the BaseQuery to help the soft deletion
# make the search has default value statue = 1
class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)




class Base(db.Model):
    __abstract__ = True
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)


    def __init__(self):
        self.create_time = int(datetime.now().timestamp())


    def set_attrs(self, attrs_dict):
        for k,v in attrs_dict.items():
            if hasattr(self, k) and k != 'id':
                setattr(self, k, v)

    @property
    def create_datatime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0
