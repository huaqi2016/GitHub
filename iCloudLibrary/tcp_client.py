#!/usr/bin/env python
#coding:utf-8
import socket
import signal
import weakref
import errno
import logging
import pyev

import tcp_message as tcp_msg

logging.basicConfig(level=logging.DEBUG)

STOPSIGNALS = (signal.SIGINT, signal.SIGTERM)
NONBLOCKING = (errno.EAGAIN, errno.EWOULDBLOCK)


class TcpConnection(object):

    def __init__(self, sock, address, loop):
        self.sock = sock
        self.address = address
        self.sock.setblocking(0)
        self.buf = ""
        self.watcher = pyev.Io(self.sock, pyev.EV_READ, loop, self.io_cb)
        self.watcher.start()
        logging.debug("{0}: connection is ready".format(self))

    def reset(self, events):
        self.watcher.stop()
        self.watcher.set(self.sock, events)
        self.watcher.start()

    def handle_error(self, msg, level=logging.ERROR, exc_info=True):
        logging.log(level, "{0}: {1} --> connection is closing".format(self, msg),
                    exc_info=exc_info)
        self.close()

    def handle_read(self):
        try:
            buf = self.sock.recv(10240)
        except socket.error as err:
            if err.args[0] not in NONBLOCKING:
                self.handle_error("Error reading from {0}".format(self.sock))
        if buf:
            self.buf += buf
            self.reset(pyev.EV_READ | pyev.EV_WRITE)
        else:
            self.handle_error("Connection closed by peer", logging.DEBUG, False)

    def handle_write(self):
        try:
            sent = self.sock.send(self.buf)
        except socket.error as err:
            if err.args[0] not in NONBLOCKING:
                self.handle_error("Error writing to {0}".format(self.sock))
        else :
            self.buf = self.buf[sent:]
            if not self.buf:
                self.reset(pyev.EV_READ)

    def io_cb(self, watcher, revents):
        if revents & pyev.EV_READ:
            self.handle_read()
        elif revents & pyev.EV_WRITE:
            self.handle_write()
        else:
            self.handle_error("Received unkown pyev events: {0}".format(revents))

    def close(self):
        self.sock.close()
        self.watcher.stop()
        self.watcher = None
        logging.debug("{0}: connection is closed".format(self))


class TcpClient(object):

    def __init__(self, address):
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(address)
        self.sock.setblocking(0)
        self.address = self.sock.getsockname()
        self.loop = pyev.default_loop()
        self.watchers = [pyev.Signal(sig, self.loop, self.stop_signal_cb)
                         for sig in STOPSIGNALS]
        self.watchers.append(pyev.Io(self.sock, pyev.EV_READ, self.loop,
                                     self.io_cb))
        self.conns = weakref.WeakValueDictionary()

    def handle_error(self, msg, level=logging.ERROR, exc_info=True):
        logging.log(level, "{0}: {1} --> stopping".format(self, msg),
                    exc_info=exc_info)
        self.stop()

    def stop_signal_cb(self, watcher, revents):
        self.stop()

    def io_cb(self, watcher, revents):
        try:
            while True:
                try:
                    sock, address = self.sock.accept()
                except socket.error as err:
                    if err.args[0] in NONBLOCKING:
                        break
                    else:
                        raise
                else:
                    self.conns[address] = TcpConnection(sock, address, self.loop)
        except Exception:
            self.handle_error("Error accepting a connection")

    def start(self):
        self.sock.listen(socket.SOMAXCONN)
        for watcher in self.watchers:
            watcher.start()
        logging.debug("{0}: started on {0.address}".format(self))
        self.loop.start()

    def stop(self):
        self.loop.stop(pyev.EVBREAK_ALL)
        self.sock.close()
        while self.watchers:
            self.watchers.pop().stop()
        for conn in self.conns.values():
            conn.close()
        logging.debug("{0}: stopped".format(self))


if __name__ == "__main__":
    client = TcpClient(("", 9876))
    client.start()
