import argparse
import sys
import socket
import os
import threading
import listener
import connection
from crypt_image import CryptImage
from card import Card


threads = list()

    

def run_server(ip,port,dir):
    with listener.Listener(ip,port) as serv:
        while True:
            #When we get a message
            conn = serv.accept()
            if conn:
                conn.receive_message(dir)


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('dir',type=str, help='the directory to save the image')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        print(args.server_ip, args.server_port)
        run_server(args.server_ip, args.server_port,args.dir)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())