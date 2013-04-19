__version__ = '0.1'

import socket
import fcntl
import struct
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.app import App
from android import AndroidService

app = None

Builder.load_string('''
<MainScreen>:
    Image:
        source: 'background.png'
        allow_stretch: True
        keep_ratio: False
    BoxLayout:
        size_hint_y: .2
        pos_hint: {'top': 1}
        canvas:
            Color:
                rgba: .1, .1, .1, .1
            Rectangle:
                pos: self.pos
                size: self.size
        Widget
        Image:
            source: 'icon.png'
            mipmap: True
            size_hint_x: None
            width: 100
        Label:
            text: 'Remote Kivy'
            font_size: 30
            size_hint_x: None
            width: self.texture_size[0] + 20
        Widget
    Label:
        text: 'ssh -p8000 admin@{0}'.format(root.lan_ip)
        font_size: 20
        size_hint_y: .6
    Button:
        text: 'Exit'
        size_hint: .4, .1
        pos_hint: {'center_x': .5}
        on_press: app.quit_app()
''')


class MainScreen(FloatLayout):
    lan_ip = StringProperty('127.0.0.1')

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        ip = socket.gethostbyname(socket.gethostname())
        if ip.startswith('127.'):
            interfaces = ['eth0', 'eth1', 'eth2', 'wlan0', 'wlan1', 'wifi0',
                    'ath0', 'ath1', 'ppp0']
            for ifname in interfaces:
                try:
                    ip = self.get_interface_ip(ifname)
                    break
                except IOError:
                    pass
        self.lan_ip = ip

    def get_interface_ip(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', ifname[:15])
            )[20:24])


class RemoteKivyApp(App):
    def build(self):
        global app
        app = self
        self.service = AndroidService('Kivy Remote Shell',
                                      'remote shell is running')
        self.service.start('8000')
        return MainScreen()

    def quit_app(self):
        self.service.stop()
        self.stop()

if __name__ == '__main__':
    RemoteKivyApp().run()
