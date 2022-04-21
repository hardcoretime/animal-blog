from sqlalchemy.orm import sessionmaker, scoped_session, Session as SessionType
from string import Template
from init_blog_db import engine, User, Post

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

USERS = ['Aleksandr', 'Nikolay', 'Dmitriy', 'Petr', 'Artyom']
POST_TITLES = ['Lion', 'Wolf', 'Fox', 'Tiger', 'Beaver']
TEXT_TEMPLATE = Template('Some interesting text about $animal.')


def create_user(session: SessionType, name: str) -> User:
    user = User(username=name)

    session.add(user)
    session.commit()

    return user


def create_post(session: SessionType, title: str, author: str, text: str) -> Post:
    post = Post(title=title, author=author, text=text)

    session.add(post)
    session.commit()

    return post


def main() -> None:
    session = Session()

    for user in USERS:
        create_user(session, user)

    for user, title in zip(USERS, POST_TITLES):
        create_post(session, title, user, TEXT_TEMPLATE.substitute(animal=title))

    additional_post_title = 'Elephant'
    additional_post_author = USERS[0]
    create_post(
        session, additional_post_title, additional_post_author, TEXT_TEMPLATE.substitute(animal=additional_post_title)
    )

    session.close()


if __name__ == '__main__':
    main()
