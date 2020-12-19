import os
import socket
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname('__file__'), '.env')
load_dotenv(dotenv_path)
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
TOKEN = os.getenv('TOKEN')
NICK = os.getenv('NICK')
CHANNEL = os.getenv('CHANNEL')


class TwitchBot:
    def __init__(self, host=HOST, port=PORT, token=TOKEN, nick=NICK, channel=CHANNEL):
        self.s = socket.socket()
        self.host = host
        self.port = port
        self.token = token
        self.nick = nick
        self.channel = channel

    def __pong__(self):
        self.s.send(f"PONG :tmi.twitch.tv\r\n".encode('utf-8'))

    def connect(self):
        self.s.connect((self.host, int(self.port)))
        self.s.send(f"PASS {self.token}\r\n".encode('utf-8'))
        self.s.send(f"NICK {self.nick}\r\n".encode('utf-8'))
        print(self.read_messages())

    def join_channel(self, channel_=None):
        if channel_:
            self.s.send(f"JOIN #{channel_}\r\n".encode('utf-8'))
        else:
            self.s.send(f"JOIN #{self.channel}\r\n".encode('utf-8'))

    def send_message(self, message: str, channel_=None):
        if not channel_:
            channel_ = self.channel

        self.s.send(f"PRIVMSG #{channel_} :{message}\r\n".encode('utf-8'))

    def read_messages(self):
        response = self.s.recv(1024).split(b'\r\n')
        diff = "utf-8 " * len(response)

        return '\n'.join(list(map(str, response, diff.split(' '))))