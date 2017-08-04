

import argparse
import json
import os
import socket
import sys
import time


def get_dir_index(path):
    """
    :param path: Path to folder with files
    :return: dict(
                  'files': list(<path to file>:str),
                  'index':dict((<path to file>: str): <last changed time>: float),
                  'sizes': dict((<path to file>: str):<file size>: int)
                  )
    """
    files = []
    index = {}
    sizes = {}

    for root, _, filenames in os.walk(path):
        for f in filenames:
            files.append(os.path.join(root, f).replace('\\', '/'))

    for f in files:
        index[f] = os.path.getmtime(os.path.join(path, f))
        sizes[f] = os.path.getsize(os.path.join(path, f))
    return dict(files=files, index=index, sizes=sizes)


def compute_diff(dict_new, dict_old):
    """
    Returns dict with paths to created, deleted and updated files.
    :param dict_new: dict() from get_dir_index(), computed second
    :param dict_old: dict() from get_dir_index(), computed first
    :return:
        dict(
            'created': list(<path to created file>: str)
            'deleted': list(<path to deleted file>: str)
            'updated': list(tuple(
                                  <path to changed file>: str,
                                  <old file size>: int,
                                  <new file size>: int)
                                  )
            )
    """
    data = {}
    data['created'] = list(set(dict_new['files'])-set(dict_old['files']))
    data['deleted'] = list(set(dict_old['files'])-set(dict_new['files']))
    data['updated'] = []

    for f in set(dict_new['files']).intersection(set(dict_old['files'])):
        if dict_old['index'][f] != dict_new['index'][f]:
            data['updated'].append((f, dict_old['sizes'][f], dict_new['sizes'][f]))
    return data


def send_msg(sock, msg):
    """
    Protocol to send data.
    :param sock: socket to send :msg: to
    :param msg: message to send
    """
    size_of_package = sys.getsizeof(msg)
    package = str(size_of_package)+'|'+str(msg)
    sock.send(package.encode('utf-8'))


def main(loop_time, path, ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Set up TCP socket
        s.connect((ip, port))

    except Exception as e:
        print(e)
    else:
        while 1:
            diff_old = get_dir_index(path)
            time.sleep(loop_time)
            diff_new = get_dir_index(path)
            # if something is changed
            if sum(diff_new['index'].values()) != sum(diff_old['index'].values()):
                a = compute_diff(diff_new,diff_old)
                # Output example
                for each in a:
                    print(each.capitalize() + ':\n')
                    for i in a[each]:
                        if len(i) == 3:
                            print(i[0] + '\n')
                            print('Old size: {} bytes\nNew size: {} bytes\n'.format(i[1], i[2]))
                        else:
                            print(i + '\n')
                send_msg(s,json.dumps(a)) # sends json-formatted string to the socket


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='Folder to scan.')
    parser.add_argument('--ip', metavar='127.0.0.1', type=str, default='localhost', help='Server ip address.')
    parser.add_argument('--port', metavar='9812', type=int, default=9812, help='Server port.')
    parser.add_argument('--loop', metavar='2', type=int, default=2, help='Time between directory scans(in seconds).')
    args = parser.parse_args()

    main(path=args.path, ip=args.ip, port=args.port, loop_time=args.loop)
