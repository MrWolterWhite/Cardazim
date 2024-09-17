import argparse
import sys
import socket
import os
import threading

def handle_connection(socket):
    lock = threading.Lock()

    from_client = ''
    try:
        with lock:
            msg_size = socket.recv(4).decode('utf-8')
            if msg_size:
                msg_size = int(msg_size)
                data = socket.recv(msg_size).decode('utf-8')       
                if data:
                    from_client += data
                    #print(f"Connection from {serv.getsockname()[0]}:{serv.getsockname()[1]} to {conn.__repr__()[(conn.__repr__().index(')')+11):-2].replace("\', ",":")}")
                    print(f"From client: {from_client}")
                    
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")
    finally:
        if socket:
            socket.close()


class Connection:
    def __init__(self, connection: socket.socket):
        self.connection = connection

    def __repr__(self):
        return f"Connection from {self.connection.getsockname()[0]}:{self.connection.getsockname()[1]} to {self.connection.__repr__()[(self.connection.__repr__().index(')')+11):-2].replace("\', ",":")}"
    def send_message(self, messege: bytes):
        str_messege = messege.decode()
        self.connection.send(len(str_messege).to_bytes(4)+messege)
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

if __name__ == "__main__":
    with Connection.connect("127.0.0.1", 8080) as connection:
        connection.send_message(b'hello')
        data = connection.receive_message()
