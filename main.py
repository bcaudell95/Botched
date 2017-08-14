import socket
import sys

# Code taken from https://stackoverflow.com/questions/2968408/how-do-i-program-a-simple-irc-bot-in-python

server = "irc.chat.twitch.tv"
port = 6667
channel = "#bcaudell95"
botnick = "bcaudell95"
password = "oauth:n6l2nqldup6ki5kc5ljw6osw05meg6"

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("connecting to:{}".format(server))
irc.connect((server, port))
irc.send("USER {} {} {} :testbot\n".format(botnick, botnick, botnick).encode())
irc.send("PASS {}\n".format(password).encode())
irc.send("NICK {}\n".format(botnick).encode())
irc.send("PRIVMSG nickserv :iNOOPE\r\n".encode())
irc.send("JOIN {}\r\n".format(channel).encode())

try:
    while 1:
        text = irc.recv(2040).decode()
        print("{}\n".format(text))

        if 'PING' in text:
            irc.send('PONG {}\r\n'.format(text.split()[1]).encode())
        elif 'PRIVMSG' in text:
            user, msg = text.split('PRIVMSG')[1].split(':')
            user = user[2:]
            msg = msg[:-2]
            print("Found message: {} from {}".format(msg, user))
finally:
    irc.send("PART {}".format(channel))
