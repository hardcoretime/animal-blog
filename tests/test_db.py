from typing import List

from pytest import fixture
from sqlalchemy.orm import Session as SessionType

from fill_blog_db import Session, USERS
from init_blog_db import Post, User

AUTHOR = 'Aleksandr'
AUTHOR_POST_COUNT = 2


def query_all_posts(session: SessionType) -> List[Post]:
    return session.query(Post).all()


def query_all_users(session: SessionType) -> List[User]:
    return session.query(User).all()


def query_user_posts(session: SessionType, user: str) -> List[Post]:
    return session.query(Post).filter_by(author=user).all()


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
