from collections import namedtuple
from string import Template

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session as SessionType
from werkzeug.security import generate_password_hash

from config import DevelopmentConfig
from models import User, Post, Tag, PostsTags

engine = create_engine(
    url=DevelopmentConfig.SQLALCHEMY_DATABASE_URI, echo=True
)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

Article = namedtuple('Article', 'user_id title')
EMAIL_DOMAIN = 'example.ru'
USERS = ['Aleksandr', 'Nikolay', 'Dmitriy', 'Petr', 'Artyom']
POSTS = [
    Article(1, 'Lion'),
    Article(2, 'Wolf'),
    Article(3, 'Fox'),
    Article(4, 'Tiger'),
    Article(5, 'Beaver'),
]
TAGS = ['canidae', 'feline', 'rodent']
POSTS_TAGS_MAPPING = {
    1: 2,
    2: 1,
    3: 1,
    4: 2,
    5: 3,
}
TEXT_TEMPLATE = Template('Some interesting text about $animal.')


def create_user(session: SessionType, name: str) -> User:
    new_user = User(
        email=f'{name}@{EMAIL_DOMAIN}',
        name=name,
        password=generate_password_hash(f'{name}!', method='sha256')
    )

    session.add(new_user)
    session.commit()

    return new_user


def create_post(session: SessionType, article: Article, content: str) -> Post:
    post = Post(title=article.title, user_id=article.user_id, content=content)

    session.add(post)
    session.commit()

    return post


def create_tag(session: SessionType, name: str) -> Tag:
    tag = Tag(name=name)

    session.add(tag)
    session.commit()

    return tag


def main() -> None:
    session = Session()

    for user in USERS:
        create_user(session, user)

    for user, article in zip(USERS, POSTS):
        create_post(
            session, article, TEXT_TEMPLATE.substitute(animal=article.title)
        )

    for tag in TAGS:
        create_tag(session, tag)

    additional_article = Article(1, 'Elephant')
    create_post(
        session,
        additional_article,
        TEXT_TEMPLATE.substitute(animal=additional_article.title)
    )

    for post_id, tag_id in POSTS_TAGS_MAPPING.items():
        new_associations = PostsTags(
            post_id=post_id,
            tag_id=tag_id
        )

        session.add(new_associations)
        session.commit()

    session.close()


if __name__ == '__main__':
    main()
