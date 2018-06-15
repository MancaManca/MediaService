import socket
import threading
from datetime import datetime
from pathlib import Path
from subprocess import call

import pyperclip
from kivy._clock import CyClockBaseFree
from kivy.app import App
from kivy.clock import mainthread
from kivy.metrics import dp
from kivy.properties import Logger, Clock, partial, DictProperty
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SwapTransition, RiseInTransition, \
    CardTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex

class Connector:
    url = ''
    def __init__(self, **kwargs):
        super(Connector, self).__init__(**kwargs)
        Logger.info('Connector: Initialized {}'.format(self))


        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.url:
            self.host = self.url
            print(self.host)
        else:
            self.host = '192.168.0.10'
        self.port = 8000
        self.server_state = True

        self.connects(self.host, self.port)



    def connects(self, host, port, *args):
        try:
            # self.sock = socket.create_connection(source_address=(self.host, self.port))
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host,port))
            self.receive()
        except ConnectionRefusedError:
            print('nope')
            self.server_state = False
        except ConnectionResetError:
            print('nope reset')
            self.server_state = False
            pass


    def mysend(self, msg, *args):
        totalsent = 0
        print(self.server_state)
        if self.server_state:
            self.sock.send(msg.encode())
            self.receive()


    def receive(self, *args):
        responded_msg = self.sock.recv(2048)
        print(responded_msg.decode())
        if not len(responded_msg.decode()):
            print('false')

            self.server_state = False
            try:
                self.sock.close()
            except OSError:
                print('not able to close')
                pass
            self.connects(self.host, self.port)

        else:
            self.server_state = True
            print('true')


class Progression(Screen):
    progress_barr = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Progression, self).__init__(**kwargs)
        Logger.info('Progression: Initialized {}'.format(self))
        print(' progression {}'.format(self.parent))

        self.sch_event = Clock.schedule_interval(self.progression_bar, 1 / 20)

        # self.start_scan()


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

            self.manager.switch_to(ScanView(),transition=FadeTransition(), duration=1)



class MoviesView(Screen):
    def __init__(self, **kwargs):
        super(MoviesView, self).__init__(**kwargs)
        Logger.info('MoviesView: Initialized {}'.format(self))
        Clock.schedule_once(self.pr, 9)

    def pr(self, *args):
        print(self.parent)
        print(self.manager.screens)
        # print(' MainView {}'.format(self.parent))
        print(self.manager.screen_names)
    pass
class SeriesView(Screen):
    def __init__(self, **kwargs):
        super(SeriesView, self).__init__(**kwargs)
        Logger.info('SeriesView: Initialized {}'.format(self))
        Clock.schedule_once(self.pr, 9)

    def pr(self, *args):
        print(self.parent)
        print(self.manager.screens)
        # print(' MainView {}'.format(self.parent))
        print(self.manager.screen_names)
    pass
class SearchView(Screen):
    def __init__(self, **kwargs):
        super(SearchView, self).__init__(**kwargs)
        Logger.info('SearchView: Initialized {}'.format(self))

        Clock.schedule_once(self.pr, 9)

    def pr(self, *args):
        print(self.parent)
        print(self.manager.screens)
        # print(' MainView {}'.format(self.parent))
        print(self.manager.screen_names)

    pass

class LatestView(Screen):
    def __init__(self, **kwargs):
        super(LatestView, self).__init__(**kwargs)
        Logger.info('LatestView: Initialized {}'.format(self))

        Clock.schedule_once(self.pr, 9)

        self.connn = Connector()

    def cc(self, msg, *args):
        self.connn.mysend(msg)

    def reconnect(self, *args):
        self.connn.connects(self.connn.host,self.connn.port)

    def pr(self, *args):
        print(self.parent)
        print(self.manager.screens)
        # print(' MainView {}'.format(self.parent))
        print(self.manager.screen_names)

    pass

class MainViewScManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MainViewScManager, self).__init__(**kwargs)
        Logger.info('MainViewScManager: Initialized {}'.format(self))
        # self.add_widget(MoviesView(name='movies_view'))
        # self.add_widget(SeriesView(name='series_view'))
        # self.add_widget(SearchView(name='search_view'))


class MainView(Screen):
    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)
        Logger.info('MainView: Initialized {}'.format(self))
        # Clock.schedule_once(self.pr, 9)
        # self.ids.screen_m_container.add_widget(MainViewScManager())
    def pr(self, *args):
        print(self.parent)
        print(self.manager.screens)
        # print(' MainView {}'.format(self.parent))
        print(self.manager.screen_names)
        if 'settings' not  in self.manager.screen_names:

            self.manager.switch_to(SettingsView(), transition=FadeTransition())
        else:
            self.manager.current = 'settings'
    pass

class ScanView(Screen):
    urls_list = {}
    def __init__(self, **kwargs):
        super(ScanView, self).__init__(**kwargs)
        Logger.info('ScanView: Initialized {}'.format(self))
        self.llist = self.urls_list
        for it in self.llist:
            self.ids.scan_view_container.add_widget(Button(text='{}  {}'.format(it,self.llist[it]),on_release=self.set_as_host))

    def set_as_host(self, *args):
        # Connector.url = self.text[:13]
        print(self)
    def pr(self, *args):
        print(self.parent)
        print(self.manager.screens)
        # self.manager.current = 'main'
        self.manager.switch_to(MainView(), transition=FadeTransition(), duration=1)


class SettingsView(Screen):
    def __init__(self, **kwargs):
        super(SettingsView, self).__init__(**kwargs)
        Logger.info('SettingsView: Initialized {}'.format(self))
        Clock.schedule_once(self.pr, 9)

    def pr(self, *args):
        print(self.parent)
        print(self.manager.screens)
        self.manager.current = 'main'
        # print(' MainView {}'.format(self.parent))

class ViewControl(ScreenManager):
    def __init__(self, **kwargs):
        super(ViewControl, self).__init__(**kwargs)
        Logger.info('ViewControl: Initialized {}'.format(self))
        # self.add_widget(Progression(name='loading'))
        # self.add_widget(MainView(name='main'))

        self._url = []
        # self.start_loading_screen()
        self.t1 = threading.Thread(name="Hello1", target=self.start_loading_screen())
        self.t1.start()

        self.t2 = threading.Thread(target=self.scanner)
        self.t2.start()
        # self.t2.join(timeout=1)




        # self.t2.join(timeout=2)


    def start_loading_screen(self, *args):
        self.add_widget(Progression(name='loading'))

    def set_ui(self, *args):
        self.add_widget(MainView())

    def scanner(self ,*args):
        # Logger.info('entered scanner for {}'.format(threading.currentThread().getName()))
        for _subnet in range(1,15):
            Logger.info('Scanner for {}'.format(_subnet))
            network = '192.168.0.{}'.format(_subnet)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(0.1)

            try:
                _socker = sock.connect_ex((network, 8000))

                if _socker == 0:
                    Logger.info('Found online at {}'.format(network))
                    responded_msgs = sock.recv(2048)
                    ScanView.urls_list[network] = str(responded_msgs.decode())
                else:
                    Logger.info('{} responded {}'.format(network, _socker))
            except PermissionError:
                print('permission')
            except ConnectionRefusedError:
                print('Refused')
            finally:
                sock.close()
                Logger.info('Current :{} Exiting'.format(threading.currentThread().getName()))




    def set_url_set(self, *args):
        Logger.info(self._url)

class MediaServiceMclientApp(App):

    def build(self):
        Logger.info('Application : Initialized {}'.format(self))

        self.root = BoxLayout(orientation='vertical')
        return self.root

    def on_start(self):

        self.root.add_widget(ViewControl())


    def quit_app(self, *args):
        self.stop()



    def on_pause(self):
        return True


if __name__ == '__main__':
    MediaServiceMclientApp().run()

