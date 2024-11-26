#!/usr/bin/env python3

from bskytools import BskyListTool
from argparse import ArgumentParser


def init():
    p = ArgumentParser()
    subp = p.add_subparsers(dest='main_menu', required=True)
    list_parser = subp.add_parser('list')
    list_subp = list_parser.add_subparsers(dest='operation', required=True)
    add_p = list_subp.add_parser('add')
    add_p.add_argument('target_list_name')
    add_p.add_argument('file')
    fetch_p = subp.add_parser('fetch')
    fetch_subp = fetch_p.add_subparsers(dest='operation')
    f_list_p = fetch_subp.add_parser('list')
    f_list_p.add_argument('owner')
    f_list_p.add_argument('list_name')
    f_list_p.add_argument('file')
    follower_p = fetch_subp.add_parser('followers')
    follower_p.add_argument('handle')
    follower_p.add_argument('file')
    f_likes_p = fetch_subp.add_parser('likes')
    f_likes_p.add_argument('url')
    f_likes_p.add_argument('file')
    my_args = p.parse_args()
    return my_args


def main(my_args):
    with BskyListTool(cred_file='bskytools/config', token_file='bskytools/.bsky.token') as tool:
        match my_args.main_menu:
            case 'list':
                match my_args.operation:
                    case 'add':
                        tool.add_file_to_list(my_args.target_list_name, my_args.file)
                    case 'followers':
                        pass
            case 'fetch':
                match my_args.operation:
                    case 'list':
                        entrys = tool.fetch_list(my_args.list_name, my_args.owner)
                        tool.write_to_file(entrys, my_args.file)
                    case 'followers':
                        entrys = tool.fetch_followers(my_args.handle)
                        tool.write_to_file(entrys, my_args.file)
                    case 'likes':
                        entrys = tool.fetch_likes(my_args.url)
                        tool.write_to_file(entrys, my_args.file)


if __name__ == '__main__':
    my_args = init()
    main(my_args)
