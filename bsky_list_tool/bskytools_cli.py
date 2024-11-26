
from bskytools import BskyListTool
from argparse import ArgumentParser


with BskyListTool(cred_file='config', token_file='.bsky.token') as tool:
    match args.main_menu:
        case 'list':
            match args.operation:
                case 'add':
                    tool.add_file_to_list(args.target_list_name, args.file)
                case 'followers':
                    tool.get_followers(args.handle, args.file)
        case 'fetch':
            match args.operation:
                case 'list':
                    tool.backup_list(args.list_name, args.owner, args.file)
                case 'followers':
                    tool.get_followers(args.handle, args.file)
                case 'likes':
                    tool.get_likes(args.url, args.file)

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

    args = p.parse_args()

def main():
    pass

if __name__ == '__main__':
    init()
    main()
