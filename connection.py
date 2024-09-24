import argparse
import sys
import socket
import os
import threading
from crypt_image import CryptImage
from card import Card

def handle_connection(conn):
    lock = threading.Lock()

    from_client = ''
    try:
        with lock:
            msg_size_bytes = conn.recv(4)
            msg_size = int.from_bytes(msg_size_bytes)
            msg_size = int(msg_size)
            size = msg_size
            data = b''
            while size > 0:
                retreived_data = conn.recv(msg_size)
                data += retreived_data
                size -= len(retreived_data)
            card = Card.deserialize(data)
            print(str(card))

                    
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")
    finally:
        if conn:
            conn.close()


class Connection:
    def __init__(self, connection: socket.socket):
        self.connection = connection

    def __repr__(self):
        return f"Connection from {self.connection.getsockname()[0]}:{self.connection.getsockname()[1]} to {self.connection.__repr__()[(self.connection.__repr__().index(')')+11):-2].replace("\', ",":")}"
    def send_message(self, messege: bytes):
        self.connection.send(len(messege).to_bytes(4)+messege)
    def receive_message(self):
        x = threading.Thread(target=handle_connection, args=[self.connection])
        x.start()
        
        
    @classmethod
    def connect(cls, host, port):
        print(f"host: {host}, port: {port}")
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv.connect((host, port))
        conn = Connection(connection=serv)
        return conn
    
    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

