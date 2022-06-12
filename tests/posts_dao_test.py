import pytest
from app.posts.dao.posts_dao import PostsDAO
from app.config import POSTS_PATH


class TestPostsDao:

    @pytest.fixture
    def posts_dao(self):
        return PostsDAO(POSTS_PATH)

    @pytest.fixture
    def keys_expected(self):
        return {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"}

    def test_get_all_check_type(self, posts_dao):
        """ Проверяет что список постов и каждый пост верного типа """

        posts = posts_dao.get_all()

        assert type(posts) == list, "Список всех постов должен быть списком"
        assert type(posts[0]) == dict, "Каждый пост должен быть словарем"

    def test_get_all_has_keys(self, posts_dao, keys_expected):
        """ Проверяет что у всех постов верные ключи """

        posts = posts_dao.get_all()

        for post in posts:
            keys = post.keys()
            assert keys == keys_expected, f"Полученные ключи поста {post['pk']} неверны"

    def test_get_one_check_type(self, posts_dao):
        """ Проверяет что выбранный пост - словарь """

        post = posts_dao.get_by_pk(1)

        assert type(post) == dict, "Пост должен быть словарем"

    def test_get_one_has_keys(self, posts_dao, keys_expected):
        """ Проверяет что у выбранного поста верные ключи """

        post = posts_dao.get_by_pk(1)
        assert post.keys() == keys_expected, "Полученные ключи неверны"

    parameters_get_by_pk = [1, 2, 3, 4, 5, 6, 7, 8]

    @pytest.mark.parametrize("post_pk", parameters_get_by_pk)
    def test_get_by_pk_has_correct_pk(self, posts_dao, post_pk):
        """ Проверяет что номер полученного поста соответствует запрошенному """

        post = posts_dao.get_by_pk(post_pk)
        assert post["pk"] == post_pk, "Номер полученного поста не соответствует номеру запрошенного"

    def test_search_check_type(self, posts_dao):
        """ Проверяет что результат поиска список, а элементы в нем словари """

        posts = posts_dao.search("а")

        assert type(posts) == list, "Результат поиска должен быть списком"
        assert type(posts[0]) == dict, "Элементы найденные в поиске должны быть словарем"

    def test_search_has_keys(self, posts_dao, keys_expected):
        """ Проверяет что у результата поиска верные ключи """

        post = posts_dao.search("а")[0]
        post_keys = set(post.keys())

        assert post_keys == keys_expected, "Полученные ключи неверны"

    queries_and_responses = [
        ("еда", [1]),
        ("дом", [2, 7, 8]),
        ("а", list(range(1, 8 + 1)))
    ]

    @pytest.mark.parametrize("query, posts_pks_correct", queries_and_responses)
    def test_search_correct_match(self, posts_dao, query, posts_pks_correct):
        """ Проверяет что поиск по запросу query выполняется верно """

        posts = posts_dao.search(query)
        posts_pks = [post["pk"] for post in posts]

        assert posts_pks == posts_pks_correct, f"Неверный поиск по запросу {query}"

    def test_get_by_username_check_type(self, posts_dao):
        """ Проверяет что у результата поиска по пользователю верный тип данных """

        posts = posts_dao.get_by_username("leo")

        assert type(posts) == list, "Результат поиска должен быть списком"
        assert type(posts[0]) == dict, "Элементы найденные в поиске по пользователю должны быть словарем"

    def test_get_by_username_has_keys(self, posts_dao, keys_expected):
        """ Проверяет что у результата поиска по пользователю верные ключи """
        post = posts_dao.get_by_username("leo")[0]
        post_keys = set(post.keys())

        assert post_keys == keys_expected, "Полученные ключи неверны"

    parameters_to_get_by_username = [
        ("leo", [1, 5]),
        ("johnny", [2, 6]),
        ("hank", [3, 7]),
        ("larry", [4, 8])
    ]

    @pytest.mark.parametrize("username, posts_pks", parameters_to_get_by_username)
    def test_get_by_username_correct_match(self, posts_dao, username, posts_pks):
        """ Проверяет что поиск по пользователю работает верно """

        posts = posts_dao.get_by_username(username)
        posts_keys = [post["pk"] for post in posts]

        assert posts_keys == posts_pks, f"Неверный поиск по запросу {username}"
