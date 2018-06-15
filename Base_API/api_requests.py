from inspect import signature

import requests


class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)


class api:

    def __init__(self, name):
        self.name = name

        # self.summoner()
        # self.context = None

    # def summoner(self):
    #     print('called')
    #     if self.action == 'movies':
    #         self.get_movies()
    #     if self.action == 'shows':
    #         self.get_shows()
    #     if self.action == 'search':
    #         self.query_shows()

    def _url(self, path):
        return 'https://tv-v2.api-fetch.website' + path

    # def get_movies(self):
    #     self.context = requests.get(self._url(self.movies_url))
    #
    # def get_shows(self):
    #     self.context = requests.get(self._url(self.shows_url))
    #
    # def query_shows(self):
    #     print(self._url(self.shows_url + '1?sort=name&order=1&keywords={}'.format(self.query)))
    #     self.context = requests.get(self._url(self.shows_url + '/1?sort=name&order=1&keywords={}'.format(self.query)))
    #     # print(self.context)

    def take_context(self):
        return self.context


class Movies(api):
    def __init__(self, page=None, sort=None, order=None, keywords=None, id=None, **kwargs):
        super(api, self).__init__(**kwargs)



class Shows(api):
    def __init__(self, page=None, sort=None, order=None, keywords=None, id=None, genre=None, **kwargs):
        super(api, self).__init__(**kwargs)
        self.url = self._url('/shows')
        self.query = {}
        if page:
            self.query['page'] = page
        if sort:
            self.query['sort'] = sort
        if order:
            self.query['order'] = order
        if id:
            self.query['id'] = id
        if id:
            self.query['genre'] = genre
        if keywords:
            self.query['keywords'] = str(keywords).replace(' ','%20')
        # self.get_shows()
        # self.bla()

    # def set_query(self):
    #     if page:
    #         self.query.append()
    def get_shows(self):
        self.context = requests.get(self.url)

    def get_search_shows(self):
        self.query_str = '/'
        if 'page' not in self.query:
            self.page = '1'
            self.query_str += self.page + '?'
        else:
            self.query_str = self.query_str + self.query['page'] + '?'

        for i in self.query:
            if i != 'id' and i != 'page':
                self.query_str = self.query_str + str(i) + '=' + str(self.query[i]) + '&'

        self._url_prepared = self.url + self.query_str[:-1]

        print(self._url_prepared)
        return requests.get(self._url_prepared)


# def describe_task(task_id):
#     return requests.get(_url('/tasks/{:d}/'.format(task_id)))
#
# def add_task(summary, description=""):
#     return requests.post(_url('/tasks/'), json={
#         'summary': summary,
#         'description': description,
#         })
#
# def task_done(task_id):
#     return requests.delete(_url('/tasks/{:d}/'.format(task_id)))
#
# def update_task(task_id, summary, description):
#     url = _url('/tasks/{:d}/'.format(task_id))
#     return requests.put(url, json={
#         'summary': summary,
#         'description': description,
#         })


# resp = api('movie', 'movies').take_context()
# if resp.status_code != 200:
#     raise APIError(resp.status_code)
# # print(resp.headers)
# # print(resp.content)
# # print(resp.encoding)
# # print(resp.url)
# if 'application/json' in resp.headers['Content-Type']:
#     print(resp.headers.values())
#     print('json')
# print('Got response: {}'.format(resp.json()))

# pippp = Shows(genre='animation', order='1', sort='name').get_shows_page()\
pippp = Shows(keywords='once upon a time', order='1', sort='name').get_search_shows()

print('Got response: {}'.format(pippp.json()))

# resp = todo.get_tasks()
# if resp.status_code != 200:
#     raise ApiError('Cannot fetch all tasks: {}'.format(resp.status_code))
# for todo_item in resp.json():
#     print('{} {}'.format(todo_item['id'], todo_item['summary']))
