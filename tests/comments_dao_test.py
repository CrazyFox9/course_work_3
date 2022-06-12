import pytest
from app.posts.dao.coments_dao import CommentsDAO
from app.config import COMMENTS_PATH


class TestCommentsDao:

    @pytest.fixture
    def comments_dao(self):
        return CommentsDAO(COMMENTS_PATH)

    parameters_for_comments_by_post = [
        (1, [1, 2, 3, 4]),
        (2, [5, 6, 7, 8]),
        (3, [9, 10, 11, 12])
    ]

    @pytest.mark.parametrize("post_pk, comments_pk_correct", parameters_for_comments_by_post)
    def test_get_comments_by_post_pk_check_match(self, comments_dao, post_pk, comments_pk_correct):
        """ Проверяет что получение комментов к посту работает верно """

        comments = comments_dao.get_comments_by_post_pk(post_pk)
        comments_pk = [comment["pk"] for comment in comments]

        assert comments_pk == comments_pk_correct, "Неверно выводятся комментарии к посту"

    def test_get_comments_by_post_pk_check_type(self, comments_dao):
        """ Проверяет что список комментов и каждый коммент верного типа """

        comments = comments_dao.get_comments_by_post_pk(1)

        assert type(comments) == list, "Список комментов должен быть списком"
        assert type(comments[0]) == dict, "Каждый коммент должен быть словарем"
