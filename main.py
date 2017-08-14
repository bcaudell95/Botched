import socket
import sys

# Code taken from https://stackoverflow.com/questions/2968408/how-do-i-program-a-simple-irc-bot-in-python

class BasicBot:
    SERVER = "irc.chat.twitch.tv"
    PORT = 6667

    def __init__(self, channel, nick, oauth, server=None, port=None):
        self._server = server if server is not None else BasicBot.SERVER
        self._port = port if port is not None else BasicBot.PORT
        self._channel = channel
        self._nick = nick
        self._oauth = oauth

        self._irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("connecting to:{}".format(self._server))

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        self._irc.connect((self._server, self._port))
        self._irc.send("USER {} {} {} :testbot\n".format(*([self._nick] * 3)).encode())
        self._irc.send("PASS {}\n".format(self._oauth).encode())
        self._irc.send("NICK {}\n".format(self._nick).encode())
        self._irc.send("PRIVMSG nickserv :iNOOPE\n".encode())
        self._irc.send("JOIN {}\n".format(self._channel).encode())

    def main_loop(self):
        text = self._irc.recv(2040).decode()
        print("{}\n".format(text))

        if 'PING' in text:
            self._irc.send('PONG {}\r\n'.format(text.split()[1]).encode())
        elif 'PRIVMSG' in text:
            user, msg = text.split('PRIVMSG')[1].split(':')
            user = user[2:]
            msg = msg[:-2]
            print("Found message: {} from {}".format(msg, user))

    def disconnect(self):
        self._irc.send("PART {}".format(self._channel))


def main():
    channel = "#bcaudell95"
    botnick = "bcaudell95"
    password = "oauth:n6l2nqldup6ki5kc5ljw6osw05meg6"

    with BasicBot(channel, botnick, password) as bot:
        while True:
            bot.main_loop()


main()
