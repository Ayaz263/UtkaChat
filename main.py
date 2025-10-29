import socket
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen

class ConnectScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.ip_input = TextInput(
            multiline=False,
            hint_text='Введите IP-адрес сервера',
            size_hint_y=0.1
        )
        self.name_input = TextInput(
            multiline=False,
            hint_text='Введите ваше имя',
            size_hint_y=0.1
        )
        connect_button = Button(text='Подключиться', size_hint_y=0.1)
        connect_button.bind(on_press=self.connect_to_chat)

        layout.add_widget(Label(text='Настройки подключения', size_hint_y=None, height=40))
        layout.add_widget(self.ip_input)
        layout.add_widget(self.name_input)
        layout.add_widget(connect_button)
        self.add_widget(layout)

    def connect_to_chat(self, instance):
        ip = self.ip_input.text
        name = self.name_input.text
        if ip and name:
            self.manager.get_screen('chat').setup_connection(ip, name)
            self.manager.current = 'chat'

class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.s = None
        self.host = ''
        self.port = 50000
        self.user_name = ''

        self.layout = BoxLayout(orientation='vertical')

        self.history_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        self.history_view = ScrollView()
        self.history_view.add_widget(self.history_layout)
        self.layout.add_widget(self.history_view)

        self.input_layout = BoxLayout(size_hint_y=0.1)
        self.text_input = TextInput(multiline=False, size_hint_x=0.8)
        self.send_button = Button(text='Отправить', size_hint_x=0.2)
        self.send_button.bind(on_press=self.send_message)
        self.input_layout.add_widget(self.text_input)
        self.input_layout.add_widget(self.send_button)
        self.layout.add_widget(self.input_layout)

        self.add_widget(self.layout)

    def setup_connection(self, ip, name):
        self.host = ip
        self.user_name = name
        threading.Thread(target=self.connect_to_server, daemon=True).start()

    def connect_to_server(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.host, self.port))
            self.display_message('Успешно подключено к серверу.')
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            self.display_message(f'Ошибка подключения: {e}')

    def receive_messages(self):
        while True:
            try:
                message = self.s.recv(1024).decode('utf-8')
                if message:
                    Clock.schedule_once(lambda dt: self.display_message(message))
            except Exception:
                Clock.schedule_once(lambda dt: self.display_message('Соединение с сервером потеряно.'))
                self.s.close()
                break

    def send_message(self, instance):
        message = self.text_input.text
        if message:
            try:
                full_message = f"[{self.user_name}]: {message}"
                self.s.sendall(full_message.encode('utf-8'))
                self.text_input.text = ''
            except Exception as e:
                self.display_message(f'Не удалось отправить сообщение: {e}')
                if self.s:
                    self.s.close()

    def display_message(self, message):
        label = Label(text=message, size_hint_y=None, height=40, halign='left', valign='middle')
        label.bind(size=lambda *x: label.setter('text_size')(label, (label.width, None)))
        self.history_layout.add_widget(label)

class ChatApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ConnectScreen(name='connect'))
        sm.add_widget(ChatScreen(name='chat'))
        return sm

if __name__ == '__main__':
    ChatApp().run()
