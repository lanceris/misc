import socket
import threading
import json
from time import gmtime, strftime
import sys

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host,self.port))

    def listen(self):
        self.sock.listen(5)
        while 1:
            client, addr = self.sock.accept()
            #client.settimeout(60)
            threading.Thread(target=self.listenToClient, args=(client,addr)).start()
    def listenToClient(self, client, addr):
        print('New client: {}:{}'.format(addr[0], addr[1]))
        while 1:
            try:
                msg_size, msg = ThreadedServer.recv_msg(client)
            except:
                print('{}:{} has ended session.'.format(addr[0], addr[1]))
                break
            try:
                d = json.loads(msg, strict=False)
            except Exception as e:
                print(e)
            with open('{}.log'.format(strftime("%d-%m-%Y", gmtime())),'a', encoding='utf-8') as log:
                log.write(strftime("%d-%m-%Y %H:%M:%S\n", gmtime()))
                log.write('Received data from {}:{}\n'.format(addr[0], addr[1]))
                for each in d:
                    log.write(each.capitalize() + ':\n')
                    for i in d[each]:
                       if len(i) == 3:
                           log.write(i[0]+'\n')
                           log.write('Old size: {} bytes\nNew size: {} bytes\n'.format(i[1], i[2]))
                       else:
                           log.write(i+'\n')
                log.write('<<<================>>>\n')


    @staticmethod
    def recv_msg(sock):
        """Receives message"""
        try:
            header = sock.recv(2).decode('utf-8')                           #Start from small number
            while '|' not in header:
                header += sock.recv(1).decode('utf-8')                      #Increase received message until it hits the delimiter
            size_of_package, sep, msg_fragment = header.partition("|")
            msg = sock.recv(int(size_of_package)).decode('utf-8')
            full_msg = msg_fragment + msg
            return size_of_package,full_msg
        except OverflowError as e:
            print(e)
        except:
            print('Unexpected error:', sys.exc_info()[0])

server_ip = '192.168.0.38'

if __name__ == '__main__':
    print('Server started.')
    print('Waiting for clients...')
    a = ThreadedServer('localhost',8888)
    a.listen()

