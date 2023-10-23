import argparse, getpass
from time import time
from argparse import ArgumentParser, Namespace
from typing import Any
from tqdm import tqdm
from cryptography.fernet import InvalidToken
from getpass4 import getpass
from crypto import Encryption, Decryption, Append
import pathlib


class Password(argparse.Action):
    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: Any, optional_string):
        if values is None:
            values = getpass(prompt='Enter your password: ')
        setattr(namespace, self.dest, values)


def file_name(value: str):
    if value.endswith(('.txt', '.encrypted')):
        return value
    return argparse.ArgumentError()


def main(args_from_user):
    files_to_process = args_from_user.file
    if args_from_user.verbose >= 3:
        files_to_process = tqdm(args_from_user.file)
    for file in files_to_process:
        before = time()
        path = pathlib.Path(file)
        if args_from_user.mode == 'encrypt':
            action = Encryption(path)
        elif args_from_user.mode == 'decrypt':
            action = Decryption(path)
        elif args_from_user.mode == 'append':
            text = input('Jaki tekst dopisać do pliku? ')
            action = Append(path, text)
        try:
            if not action.execute(args_from_user.password):
                continue
        except InvalidToken:
            print(f'Wrong password for: {file}')
            continue
        after = time()
        if 0 < args_from_user.verbose <= 2:
            print(f'File: {file}', end='')
            if args_from_user.verbose > 1:
                print(f' -> job done in {round((after - before), 2)} seconds', end='')
            print()
        elif args_from_user.verbose >= 3:
            files_to_process.set_description(file)


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
