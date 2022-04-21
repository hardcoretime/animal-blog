import os
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base

LOGIN = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')
PORT = os.getenv('PORT', default=5432)
DB_NAME = os.getenv('DB_NAME', default='blog')
DB_URL = f'postgresql+pg8000://{LOGIN}:{PASSWORD}@localhost:{PORT}/{DB_NAME}'
DB_ECHO = True

engine = create_engine(url=DB_URL, echo=DB_ECHO)


class Base:
    id = Column(Integer, primary_key=True)


Base = declarative_base(bind=engine, cls=Base)


class User(Base):
    __tablename__ = 'users'

    username = Column(String(30), unique=True)
    verified = Column(Boolean, default=False, nullable=False)
    registration_date = Column(DateTime, default=datetime.utcnow)

    def change_verified(self, status: bool) -> None:
        self.verified = status

    def __str__(self):
        return f'{self.__class__.__name__}({self.username}, {self.verified}, {self.registration_date})'

    def __repr__(self):
        return str(self)


class Post(Base):
    __tablename__ = 'posts'

    title = Column(String(30), unique=False)
    author = Column(String(30), ForeignKey('users.username', ondelete='CASCADE'), nullable=False)
    tag = Column(String(30), ForeignKey('tags.name', ondelete='CASCADE'))
    text = Column(String, unique=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    def __str__(self):
        return f'{self.__class__.__name__}({self.title}, {self.author})'

    def __repr__(self):
        return str(self)


class Tag(Base):
    __tablename__ = 'tags'

    name = Column(String(30), unique=True, nullable=False)

    def __str__(self):
        return f'{self.__class__.__name__}({self.name})'

    def __repr__(self):
        return str(self)


def main():
    Base.metadata.create_all()


if __name__ == '__main__':
    main()