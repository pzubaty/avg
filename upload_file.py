#!/usr/bin/env python3
"""Upload file defined to URL
"""
import argparse
import requests

def main():
    parser = argparse.ArgumentParser(
        description=('Upload file to a server specified by URL'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u', '--url', dest='url',
                        help='server url',
                        default='http://localhost:5000/upload', type=str)
    parser.add_argument('-f', '--filename', dest='filename',
                        help='file to send',
                        default='', type=str)
    args = parser.parse_args()

    send_file(args.url, args.filename)


def send_file(url, filename):
    """Send file defined by filename to the server defined by url

    :param url: server url incl. port and protocl

    :param filename: path to the file to send

    :return: None
    """
    with open(filename, 'rb') as f:
        #files = {'pptx': f}
        files = {'file': f}

        r = requests.post(url, files=files)
        print(r.text)


if __name__ == '__main__':
    main()
