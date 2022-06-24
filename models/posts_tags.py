from .database import db


class PostsTags(db.Model):
    # __tablename__ = 'posts_tags'
    post_id = db.Column(
        db.Integer, db.ForeignKey('posts.id'), primary_key=True
    )
    tag_id = db.Column(
        db.Integer, db.ForeignKey('tags.id'), primary_key=True
    )
