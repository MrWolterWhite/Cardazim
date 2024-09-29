import argparse
import sys
import socket
import connection
import listener
from crypt_image import CryptImage
from card import Card



###########################################################
####################### YOUR CODE #########################
###########################################################


def send_data(server_ip, server_port, data):
    '''
    Send data to server in address (server_ip, server_port).
    '''

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((server_ip, int(server_port)))

    client = connection.Connection(server)

    client.send_message(data)
    
    client.close()


###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('name', type=str,
                        help='the name of the card')
    parser.add_argument('creator', type=str,
                        help='the name of the creator')
    parser.add_argument('riddle', type=str,
                        help='the riddle')
    parser.add_argument('solution', type=str,
                        help='the solution to the riddle')
    parser.add_argument('path', type=str,
                        help='the path of the image')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        card = Card.create_from_path(args.name, args.creator, args.path, args.riddle, args.solution)
        card.image.encrypt(args.solution)
        send_data(args.server_ip, args.server_port, card.serialize())
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())