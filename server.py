import argparse
import sys
import socket
import os
import threading
import listener
import connection


threads = list()

def handle_connection(conn):
    serv = conn.connection
    lock = threading.Lock()

    from_client = ''
    try:
        with lock:
            msg_size = int.from_bytes(serv.recv(4))
            if msg_size:
                msg_size = int(msg_size)
                data = serv.recv(msg_size).decode('utf-8')       
                if data:
                    from_client += data
                    #print(f"Connection from {serv.getsockname()[0]}:{serv.getsockname()[1]} to {conn.__repr__()[(conn.__repr__().index(')')+11):-2].replace("\', ",":")}")
                    print(f"From client: {from_client}")
                    
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")
    finally:
        if serv:
            conn.close()
    

def run_server(ip,port):
    serv = listener.Listener(ip,port)
    serv.start()

    while True:
        #When we get a message
        conn = serv.accept()
        x = threading.Thread(target=handle_connection, args=[conn])
        x.start()


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        print(args.server_ip, args.server_port)
        run_server(args.server_ip, args.server_port)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())