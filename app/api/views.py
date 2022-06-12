import logging

from json import JSONDecodeError

from flask import Blueprint, render_template, abort, jsonify

from app.posts.dao.posts_dao import PostsDAO
from app.posts.dao.coments_dao import CommentsDAO
from app.config import POSTS_PATH, COMMENTS_PATH

posts_dao = PostsDAO(POSTS_PATH)
comments_dao = CommentsDAO(COMMENTS_PATH)

logger = logging.getLogger("basic")

api_blueprint = Blueprint('api_blueprint', __name__, template_folder='templates')


@api_blueprint.route('/api/posts')
def posts_all():
    logger.debug("Запрошены все посты через API")
    posts = posts_dao.get_all()
    return jsonify(posts)


@api_blueprint.route('/api/posts/<int:post_pk>')
def post_by_id(post_pk):
    logger.debug(f"Запрошен пост {post_pk} через API")
    post = posts_dao.get_by_pk(post_pk)
    return jsonify(post)
