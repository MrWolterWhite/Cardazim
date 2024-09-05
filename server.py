import argparse
import sys
import socket


def run_server(ip,port):
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind((ip, port))
    serv.listen()
    while True:
        conn, addr = serv.accept()
        from_client = ''
        while True:
            data = conn.recv(4096)
            if not data:
                break
            from_client += data.decode('utf8')
            print(f'From client: {from_client}')
            conn.send("I am SERVER\n".encode())
        conn.close()
    print('client disconnected and shutdown')

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