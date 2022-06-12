import json


class PostsDAO:

    def __init__(self, path):
        self.path = path

    def load_data(self):
        """ Загружает данные из файла JSON"""

        with open(self.path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data

    def get_all(self):
        """ Возвращает все посты """

        return self.load_data()

    def get_by_pk(self, pk):
        """ Возвращает пост по его pk """

        posts = self.load_data()

        for post in posts:
            if post["pk"] == pk:
                return post
            elif post == posts[-1]:
                raise ValueError("Такого поста нет")

    def get_by_username(self, username):
        """ Возвращает все посты пользователя """

        posts = self.load_data()
        posts_by_user = []

        for post in posts:
            if post["poster_name"] == username:
                posts_by_user.append(post)
        if len(posts_by_user) == 0:
            raise ValueError("Такого пользователя нет")
        return posts_by_user

    def search(self, query):
        """ Возвращает посты по вхождению query """

        posts = self.load_data()
        matching_posts = []

        for post in posts:
            if query.lower() in post["content"].lower():
                matching_posts.append(post)

        return matching_posts
