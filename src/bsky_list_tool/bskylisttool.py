#!/usr/bin/env python3

from atproto import Client, IdResolver, models

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('operation')
    args = parser.parse_args()
    match args.operation:
        case 'backup':
            pass
        case 'add':
            pass