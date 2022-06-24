from collections import namedtuple
from enum import Enum
from typing import List

from pytest import fixture
from sqlalchemy.orm import Session as SessionType

from fill_blog_db import Session, USERS
from models import Post, User, PostsTags, Tag

Author = namedtuple('Author', 'id name post_count')


class Tags(Enum):
    FELINE = 'feline'
    CANIDAE = 'canidae'


FELINE = ['Lion', 'Tiger']
CANIDAE = ['Wolf', 'Fox']


def query_all_posts(session: SessionType) -> List[Post]:
    return session.query(Post).all()


def query_all_users(session: SessionType) -> List[User]:
    return session.query(User).all()


def query_user_posts(session: SessionType, user: Author) -> List[Post]:
    return session.query(Post).filter_by(user_id=user.id).all()


def query_posts_by_tags(session: SessionType):
    query = session.query(PostsTags, Post, Tag).\
        join(PostsTags, PostsTags.post_id == Post.id).\
        join(Tag, Tag.id == PostsTags.tag_id)

    records = query.all()

    return records


@fixture
def session() -> Session:
    return Session()


@fixture
def author() -> Author:
    return Author(1, 'Aleksandr', 2)


class TestBlog:

    def test_post_authors(self, session: SessionType) -> None:
        posts = query_all_posts(session)

        for post in posts:
            user = session.query(User).filter_by(id=post.user_id).first()
            assert user.name in USERS

        session.close()

    def test_users(self, session: SessionType) -> None:
        users = query_all_users(session)

        for user in users:
            assert isinstance(user, User)

        for user in users:
            assert user.name in USERS

        assert len(users) == len(USERS)

        session.close()

    def test_user_posts(self, session: SessionType, author: Author) -> None:
        user_posts = query_user_posts(session, author)

        assert len(user_posts) == author.post_count

        session.close()

    def test_tags(self, session: SessionType) -> None:
        records = query_posts_by_tags(session)

        for association, post, tag in records:
            if tag.name == Tags.FELINE.value:
                print(f'post title: {post.title} tag: {tag.name}')
                assert post.title in FELINE

            if tag.name == Tags.CANIDAE.value:
                print(f'post title: {post.title} tag: {tag.name}')
                assert post.title in CANIDAE

        session.close()
