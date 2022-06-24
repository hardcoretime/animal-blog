import logging
from typing import List

from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user

from models import Post, db, Tag, PostsTags, User, db_add_obj

log = logging.getLogger(__name__)

posts_app = Blueprint('posts_app', __name__)


@posts_app.get("/", endpoint='list')
def list_posts():
    posts: List[Post] = Post.query.all()
    return render_template('posts/list.html', posts=posts)


@posts_app.route("/<int:post_id>", methods=['GET', 'POST'], endpoint='details')
def get_post(post_id):
    if request.method == 'GET':
        post = Post.query.get_or_404(post_id)
        user = User.query.get_or_404(post.user_id)

        query = db.session.query(Post, Tag, PostsTags)
        query = query.join(PostsTags, PostsTags.post_id == Post.id)
        query = query.join(Tag, Tag.id == PostsTags.tag_id)
        records = query.filter(Post.id == post_id).all()

        tags = list()
        for _, tag, _ in records:
            tags.append(tag.name)

        return render_template(
            'posts/details.html',
            post=post,
            tags=tags,
            author=user,
        )

    if request.method == 'POST':
        existing_tags = [tag.name for tag in Tag.query.all()]
        requested_tags = request.form.get('tags').split()

        for name in requested_tags:
            if name in existing_tags:
                continue

            tag = Tag(name=name)
            db_add_obj(db, tag)

        existing_tags = Tag.query.all()
        for name in requested_tags:
            for tag in existing_tags:
                if tag.name == name:
                    posts_tags = PostsTags(post_id=post_id, tag_id=tag.id)
                    db_add_obj(db, posts_tags)

        post = Post.query.get_or_404(post_id)
        url_post = url_for(
            "posts_app.details",
            post_id=post.id,
            post_title=post.title,
            post_content=post.content,
        )
        return redirect(url_post)


@posts_app.route("/add/", methods=['GET', 'POST'], endpoint='add')
@login_required
def add_post():
    if request.method == 'GET':
        return render_template('posts/add.html')

    if request.method == 'POST':
        user = User.query.filter_by(id=current_user.id).first()

        title = request.form.get('title')
        content = request.form.get('content')

        post = Post(
            title=title,
            user_id=user.id,
            content=content,
        )
        db_add_obj(db, post)

        url_post = url_for("posts_app.details", post_id=post.id)
        flash(f"Created post {title}!")

        return redirect(url_post)
