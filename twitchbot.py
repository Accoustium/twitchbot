import os
import sqlalchemy
import socket
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname('__file__'), '.env')
load_dotenv(dotenv_path)
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
TOKEN = os.getenv('TOKEN')
NICK = os.getenv('NICK')
CHANNEL = os.getenv('CHANNEL')
DATABASE = os.getenv('DATABASE')
PING = "PING :tmi.twitch.tv\n"


class TwitchBot:
    def __init__(self, host=HOST, port=PORT, token=TOKEN, nick=NICK, channel=CHANNEL, database=DATABASE):
        self.s = socket.socket()
        self.host = host
        self.port = port
        self.token = token
        self.nick = nick
        self.channel = channel
        self.database = database

    def __enter__(self):
        self.authenticate()
        self.load_commands()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.s.close()
        self.upload_commands()

        return self

    def __load_command(self, command: str, response: str):
        self.__dict__[f"command_{command}"] = response

    def pong(self):
        self.s.send(f"PONG :tmi.twitch.tv\r\n".encode('utf-8'))

    def authenticate(self):
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
        diff = "utf-8 " * len(response[:-1])

        return '\n'.join(list(map(str, response[:-1], diff.split(' '))))

    def notice_channel(self, notice, channel_=None):
        if not channel_:
            channel_ = self.channel

        self.s.send(f"NOTICE #{channel_} :{notice}\r\n".encode('utf-8'))

    def load_commands(self):
        pass

    def upload_commands(self):
        pass
