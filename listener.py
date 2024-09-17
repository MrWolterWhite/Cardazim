import argparse
import sys
import socket
import os
import threading
import connection


class Listener:
    def __init__(self, host, port, backlog = 1000):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host,port))
    def __repr__(self):
        return f"Listener(port={self.port}, host=\'{self.host}\', backlog= {self.backlog})"
    def start(self):
        self.socket.listen()

    def stop(self):
        self.socket.close()

    def accept(self):
        conn, addr = self.socket.accept()
        return connection.Connection(conn)

    def __enter__(self):
        return self
    
    def __exit__(self):
        self.socket.close()

