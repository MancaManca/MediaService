import threading
from datetime import datetime
from pathlib import Path
from subprocess import call

import pyperclip
from kivy._clock import CyClockBaseFree
from kivy.app import App
from kivy.clock import mainthread
from kivy.metrics import dp
from kivy.properties import Logger, Clock, partial
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex


# Button.background_normal.defaultvalue = 'atlas://images/custom_atlas/dark_circle'
########################################################################################################################################################################
import hashlib
import json
import requests

hashed_dic = {}
hashed_dic_grouop = {}
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
        print(self._url_prepared)
        return requests.get(self._url_prepared)

    def get_pages(self):
        return requests.get(self.url)


class Movies(api):
    def __init__(self, page=None, sort=None, order=None, keywords=None, _id=None, genre=None, **kwargs):
        super(api, self).__init__(**kwargs)

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
        super(api, self).__init__(**kwargs)

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

def check_api_validity(_response):
    if 'application/json' not in _response.headers['Content-Type']:
        raise ApiContentError('Error response type {}'.format(_response.headers['Content-Type']))
    if _response.status_code != 200:
        raise ApiError('Error occurred: {}'.format(_response.status_code))
    # print('Got response: {}'.format(_response.json()))
    # print(json.dumps(_response.json(), sort_keys=True, indent=4))
    get_hashed_json_dic(hash_item(_response.json()))


# pippp = Shows().get_pages()
# pippp = Shows(_id = 'tt4209752').get_search_by_id()
# pippp = Shows(genre='animation', order='1', sort='name').get_search()
# pippp = Shows(page='1', order='1', sort='updated').get_search()
# pippp = Movies().get_pages()
# pippp = Movies(keywords='mission impossible', order='1', sort='name').get_search()
# pippp = Movies(_id = 'tt0120755').get_search_by_id()


def hash_item(__json_in):
    # print(type(__json_in))
    __json_hashed_out = {}
    for i in __json_in:
        # print(i['_id'])
        to_hash = 'b"{}"'.format(i['_id'])
        hashed = hashlib.sha256(to_hash.encode()).hexdigest()
        populate_hashed_table(hashed, i['_id'])
        __json_hashed_out[hashed] = i
    return __json_hashed_out

def get_hashed_json_dic(__json_hashed_in):

    for i in __json_hashed_in:

        # print('>'*90)
        # # to_hash = 'b"{}"'.format(i)
        # print('{} {} '.format(i, __json_hashed_in[i]))
        # # hashlib.sha224(to_hash).hexdigest()
        # print('>'*90)
        # print('\n')
        hashed_dic_grouop[i] = __json_hashed_in[i]

def populate_hashed_table(_key, _pair):
    hashed_dic[_key] = _pair

# check_api_validity(pippp)
# for i in hashed_dic:
#     print('{} {} '.format(i, hashed_dic[i]))
#
# for kk in hashed_dic_grouop:
#     print(hashed_dic[kk])
#     pipd = Shows(_id = hashed_dic[kk]).get_search_by_id()
#     print(json.dumps(pipd.json(), sort_keys=True, indent=4))





##########################################################################################################################################################

class Progression(BoxLayout):
    progress_barr = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Progression, self).__init__(**kwargs)
        Logger.info('Progression: Initialized {}'.format(self))

        self.sch_event = Clock.schedule_interval(self.progression_bar, 1 / 10)

    def progression_bar(self, *args):
        # Logger.info('Progression: Progress Bar progress {}'.format(self.ids.pb.value))

        # print(self.ids.zz.size_hint_x)
        if self.ids.pb.value < 100:
            self.ids.pb.value += 1
            # self.ids.dynamic_progress.size_hint_x += 0.01
            # self.ids.static_progress.size_hint_x -= 0.01
            # self.ids.dv.size_hint_x -= 0.01
            self.ids.dv.opacity -= 0.01
            self.ids.dd.opacity += 0.01
        else:
            Logger.info('Progression: Progress bar scheduler event stopped')

            self.sch_event.cancel()
            print('vsvdsvsvasvavasdv')
            print(self.parent)
            self.parent.children[0].size_hint_y = 1
            self.parent.children[0].opacity = 1
            # self.parent.remove_widget(self.parent.children[1])

class ViewControl(BoxLayout):
    def __init__(self, **kwargs):
        super(ViewControl, self).__init__(**kwargs)
        Logger.info('ViewControl: Initialized {}'.format(self))
        self.start_loading_screen()

    @mainthread
    def start_loading_screen(self, *args):
        self.add_widget(Progression())
        # self.root.add_widget(ProgressBar())

class MediaServiceMclientApp(App):
    fl = False

    def build(self):
        Logger.info('Application : Initialized {}'.format(self))

        self.root = BoxLayout(orientation='vertical')
        # self.root.size = (1300,1000)
        # self.root.add_widget(Progression())
        return self.root

    def on_start(self):
        # CyClockBaseFree.schedule_once_free(CyClockBaseFree(), self.start_loading_screen)
        # CyClockBaseFree.schedule_once_free(self.start_loading_screen)
        # self.start_loading_screen()
        # CyClockBaseFree.schedule_once_free(self.start_service)
        # print(Clock.get_boottime())
        # Clock.schedule_once(self.add_prof)
        # CyClockBaseFree.schedule_once()
        # Clock.schedule_once(self.pr_1, 1)
        # Clock.schedule_once(self.pr_2, 1)
        # Clock.schedule_once(self.start_service, 2)
        # print(CyClockBaseFree().get_events())
        # CyClockBaseFree.schedule_once_free()
        # self.th()
        self.root.add_widget(ViewControl())




        pass

    def pr_1(self, *args):
        for x in range(100):
            print('pr 1'+ str(x))
    def pr_2(self, *args):
        for x in range(100):
            print('pr 2' + str(x))
    def th(self, *args):
        self.t1 = threading.Thread(name="Hello1", target=self.add_prof)
        self.t2 = threading.Thread(name="Hello2", target=self.start_service)
        self.t1.start()
        self.t2.start()

    def add_prof(self, *args):
        self.root.add_widget(ViewControl())


    # def on_stop(self):
    #     self.profile.disable()
    #     self.profile.dump_stats('ScriptUIApp.profile')
    #
    #     import pstats
    #     p = pstats.Stats('ScriptUIApp.profile')
    #     p.strip_dirs().sort_stats(-1).print_stats()
    def start_service(self, *args):
        pippp = Shows(genre='animation', order='1', sort='name').get_search()
        check_api_validity(pippp)
        for kk in hashed_dic_grouop:
            self.get_u(kk)


        # for i in hashed_dic:
        #     print('{} {} '.format(i, hashed_dic[i]))
    def get_u(self, vz, *args):


            print(hashed_dic[vz])
            pipd = Shows(_id=hashed_dic[vz]).get_search_by_id()
            print(json.dumps(pipd.json(), sort_keys=True, indent=4))



    def quit_app(self, *args):
        self.stop()

    def on_pause(self):
        return True


if __name__ == '__main__':
    MediaServiceMclientApp().run()