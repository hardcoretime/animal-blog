from enum import Enum
from typing import List

from pytest import fixture
from sqlalchemy.orm import Session as SessionType

from fill_blog_db import Session, USERS
from init_blog_db import Post, User, Association, Tag

AUTHOR = 'Aleksandr'
AUTHOR_POST_COUNT = 2


class Tags(Enum):
    FELINE = 'feline'
    CANIDAE = 'canidae'


FELINE = ['Lion', 'Tiger']
CANIDAE = ['Wolf', 'Fox']


def query_all_posts(session: SessionType) -> List[Post]:
    return session.query(Post).all()


def query_all_users(session: SessionType) -> List[User]:
    return session.query(User).all()


def query_user_posts(session: SessionType, user: str) -> List[Post]:
    return session.query(Post).filter_by(author=user).all()


def query_posts_by_tags(session: SessionType):
    query = session.query(Association, Post, Tag)
    query = query.join(Association, Association.post_id == Post.id)
    query = query.join(Tag, Tag.id == Association.tag_id)

    records = query.all()

    return records


@fixture
def session() -> Session:
    return Session()


class TestBlog:

    def test_post_authors(self, session: SessionType) -> None:
        posts = query_all_posts(session)

        for post in posts:
            assert post.author in USERS

        session.close()

    def test_users(self, session: SessionType) -> None:
        users = query_all_users(session)

        for user in users:
            assert isinstance(user, User)

        for user in users:
            assert user.username in USERS

        assert len(users) == len(USERS)

        session.close()

    def test_user_posts(self, session: SessionType, ) -> None:
        user_posts = query_user_posts(session, AUTHOR)

        assert len(user_posts) == AUTHOR_POST_COUNT

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
