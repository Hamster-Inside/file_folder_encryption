import argparse, getpass
from argparse import ArgumentParser, Namespace
from typing import Any
from getpass4 import getpass

class Password(argparse.Action):
    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: Any, optional_string):
        if values is None:
            values = getpass(prompt='Enter your password: ')
        setattr(namespace, self.dest, values)


def file_name(value: str):
    if value.endswith('.txt'):
        return value
    return argparse.ArgumentError()

def main(args):
    print(args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Decrypt encrypt app.',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        '-m',
        '--mode',
        choices=['encrypt', 'decrypt', 'append'],
        required=True,
        help=
        '''
            encrypt -> file encryption
            decrypt -> file decryption
            append -> append text to encrypted file
        ''')

    parser.add_argument(
        '-p',
        '--password',
        required=True,
        help='Enter password',
        nargs='?',
        dest='password',
        action=Password
    )
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Level of verbose')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--file', action='append', type=file_name, help='List of file to process')
    group.add_argument('-d', '--directory', help='Path to folder with files to process')

    args = parser.parse_args()
    main(args)
