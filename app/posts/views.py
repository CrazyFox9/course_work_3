import logging

from json import JSONDecodeError

from flask import Blueprint, render_template, abort, request

from app.posts.dao.posts_dao import PostsDAO
from app.posts.dao.coments_dao import CommentsDAO
from app.config import POSTS_PATH, COMMENTS_PATH

posts_blueprint = Blueprint('posts_blueprint', __name__, template_folder='templates')
posts_dao = PostsDAO(POSTS_PATH)
comments_dao = CommentsDAO(COMMENTS_PATH)

logger = logging.getLogger("basic")


@posts_blueprint.route('/')
def posts_all():
    logger.debug("Запрошены все посты")
    try:
        posts = posts_dao.get_all()
        return render_template("index.html", posts=posts)
    except BaseException as error:
        return render_template('error.html', error="Неизвестная ошибка")


@posts_blueprint.route('/posts/<int:post_pk>')
def post_by_id(post_pk):

    try:
        post = posts_dao.get_by_pk(post_pk)
        comments = comments_dao.get_comments_by_post_pk(post_pk)
        logger.debug(f"Открыт пост {post_pk}")
    except (JSONDecodeError, FileNotFoundError) as error:
        logger.error(error)
        return render_template('error.html', error=error)
    except ValueError as error:
        logger.error(error)
        return render_template('error.html', error=error)
    except BaseException:
        logger.error("Неизвестная ошибка")
        return render_template('error.html', error="Неизвестная ошибка")

    count_comments = len(comments)

    return render_template("post.html", post=post, comments=comments, count_comments=count_comments)


@posts_blueprint.route('/search/')
def posts_search():
    query = request.args.get('s', "")

    if query != "":
        posts = posts_dao.search(query)
        count_posts = len(posts)

        logger.debug(f"Выполнен поиск по вхождению: {query}")
    else:
        posts = []
        count_posts = 0

    return render_template("search.html", posts=posts, count_posts=count_posts, query=query)


@posts_blueprint.route('/users/<username>')
def posts_by_user(username):
    try:
        posts = posts_dao.get_by_username(username)
        count_posts = len(posts)

        logger.debug(f"Открыты все посты пользователя {username}")

    except ValueError as error:
        logger.error(error)
        return render_template('error.html', error=error)

    return render_template("user-feed.html", posts=posts, count_posts=count_posts)
