import hashlib
import json
from inspect import signature


import requests

# hashed_dic = {}
# hashed_dic_grouop = {}
hashed_dic_shows = {}
hashed_dic_show = {}
hashed_dic_movie = {}
hashed_dic_movies = {}
hashed_dic_search = {}

class HashedHolder:
    def __init__(self):
        self.hashed_dic_shows = {}
        self.hashed_dic_show = {}
        self.hashed_dic_movie = {}
        self.hashed_dic_movies = {}
        self.hashed_dic_search = {}

class ApiContentError(Exception):
    """An API Content Error Exception"""

    def __init__(self, content):
        self.content = content

    def __str__(self):
        return "ApiContentError: content={}".format(self.content)

class ApiError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "ApiError: status={}".format(self.status)

class api:

    def __init__(self, name):
        self.name = name

    def _url(self, path):
        return 'https://tv-v2.api-fetch.website' + path

    def get_search(self):
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

        # print(self._url_prepared)
        return requests.get(self._url_prepared)

    def get_search_by_id(self):

        self._url_prepared = self.short_url + self.query['_id']
        # print(self._url_prepared)
        return requests.get(self._url_prepared)

    def get_pages(self):
        return requests.get(self.url)


class Movies(api):
    def __init__(self, page=None, sort=None, order=None, keywords=None, _id=None, genre=None, **kwargs):
        # super(api, self).__init__(**kwargs)

        self.url = self._url('/movies')
        self.short_url = self._url('/movie/')
        self.query = {}

        if page:
            self.query['page'] = page
        if sort:
            self.query['sort'] = str(sort).replace(' ', '%20')
        if order:
            self.query['order'] = order
        if _id:
            self.query['_id'] = _id
        if genre:
            self.query['genre'] = genre
        if keywords:
            self.query['keywords'] = str(keywords).replace(' ', '%20')

class Shows(api):
    def __init__(self, page=None, sort=None, order=None, keywords=None, _id=None, genre=None, **kwargs):
        # super(self).__init__(**kwargs)

        self.url = self._url('/shows')
        self.short_url = self._url('/show/')
        self.query = {}

        if page:
            self.query['page'] = page
        if sort:
            self.query['sort'] = str(sort).replace(' ', '%20')
        if order:
            self.query['order'] = order
        if _id:
            self.query['_id'] = _id
        if genre:
            self.query['genre'] = genre
        if keywords:
            self.query['keywords'] = str(keywords).replace(' ', '%20')

# def api_request_handler(_response):
#     if 'application/json' not in _response.headers['Content-Type']:
#         raise ApiContentError('Error response type {}'.format(_response.headers['Content-Type']))
#     if _response.status_code != 200:
#         raise ApiError('Error occurred: {}'.format(_response.status_code))
#     # print('Got response: {}'.format(_response.json()))
#     # print(json.dumps(_response.json(), sort_keys=True, indent=4))
#     get_hashed_json_dic(hash_item(_response.json()))


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

# pippp = Shows(_id = 'tt4209752').get_search_by_id()
# pippp = Shows(keywords='once upon a time', order='1', sort='name').get_search()

# print(json.dumps(pippp.json(), sort_keys=True, indent=4))

# resp = todo.get_tasks()
# if resp.status_code != 200:
#     raise ApiError('Cannot fetch all tasks: {}'.format(resp.status_code))
# for todo_item in resp.json():
#     print('{} {}'.format(todo_item['id'], todo_item['summary']))
def api_request_handler(_response):
    if 'application/json' not in _response.headers['Content-Type']:
        raise ApiContentError('Error response type {}'.format(_response.headers['Content-Type']))
    if _response.status_code != 200:
        raise ApiError('Error occurred: {}'.format(_response.status_code))
    # print('Got response: {}'.format(_response.json()))
    # print(json.dumps(_response.json(), sort_keys=True, indent=4))
    # if
    # get_hashed_json_dic(hash_item(_response.json()))


# pippp = Shows().get_pages()
pippp1 = Shows(_id = 'tt4209752').get_search_by_id()
pippp2 = Shows(genre='', order='-1', sort='name').get_search()
# pippp3 = Shows(page='1', order='1', sort='updated').get_search()
# pippp4 = Movies().get_pages()
pippp5 = Movies(keywords='mission impossible', order='-1', sort='name').get_search()
pippp6 = Movies(_id = 'tt0120755').get_search_by_id()

def item_level_():
    pass
def hash_item_m(x):
    to_hash = '{}'.format(x)
    hashed_item = hashlib.sha256(to_hash.encode()).hexdigest()
    return  hashed_item

def hash_item(__json_in, method_flag): # requires JSON object
    # print(type(__json_in))
    __json_hashed_out = {}
    if method_flag:
        print('going for multi flag {}'.format(method_flag))
        for i in __json_in:
            # print(i)
            hashed = hash_item_m(i['_id'])


            # populate_hashed_table(hashed, i['_id'])
            __json_hashed_out[hashed] = i
    else:
        print('going for multi flag {}'.format(method_flag))
        # i_for_hash = __json_in['_id']
        hashed = hash_item_m(__json_in['_id'])
        # populate_hashed_table(hashed, __json_in)
        __json_hashed_out[hashed] = __json_in



    return __json_hashed_out

def get_hashed_json_dic(__json_hashed_in, to_dic):

    for i in __json_hashed_in:

        # print('>'*90)
        # Logger.info('>'*90)
        # to_hash = 'b"{}"'.format(i)
        # Logger.info('{} {} '.format(i, __json_hashed_in[i]))
        # hashlib.sha224(to_hash).hexdigest()
        # Logger.info('>'*90)
        # Logger.info('\n')
        to_dic[i] = __json_hashed_in[i]

# def populate_hashed_table(_key, _pair):
#     hashed_dic[_key] = _pair

def api_request_controler(_api_call_response):
    if Shows().short_url in _api_call_response.url:
        get_hashed_json_dic(hash_item(_api_call_response.json(), False), hashed_dic_show)
    if Movies().short_url in _api_call_response.url:
        get_hashed_json_dic(hash_item(_api_call_response.json(), False), hashed_dic_movie)
    if Movies().url in _api_call_response.url:
        get_hashed_json_dic(hash_item(_api_call_response.json(), True), hashed_dic_movies)
    if Shows().url in _api_call_response.url:
        get_hashed_json_dic(hash_item(_api_call_response.json(), True), hashed_dic_shows)
def get_api(_api_call):
    print(_api_call.url)

    try:
        api_request_handler(_api_call)
        api_request_controler(_api_call)
    except Exception as e:
        print(e)




# api_request_handler(pippp)
get_api(pippp1)
get_api(pippp2)
# get_api(pippp3)
# get_api(pippp4)
get_api(pippp5)
get_api(pippp6)
print('work on movies')
for i in hashed_dic_movies:

    print('{} {}'.format(i, hashed_dic_movies[i]))
print('work on movie')

for i in hashed_dic_movie:

    print('{} {}'.format(i, hashed_dic_movie[i]))

print('work on shows')

for i in hashed_dic_shows:

    print('{} {}'.format(i, hashed_dic_shows[i]))

print('work on show')

for i in hashed_dic_show:

    print('{} {}'.format(i, hashed_dic_show[i]))