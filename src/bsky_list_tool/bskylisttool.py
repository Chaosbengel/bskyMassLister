#!/usr/bin/env python3

from atproto import Client, IdResolver, models
from configparser import ConfigParser, NoOptionError
from pathlib import Path
from typing import Union

class ListNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)



class BskyListTool:
    def __init__(self, handle: str=None, password: str=None, file: Union[Path,str]=None):
        if file is not Path:
            file = Path(file)
        file_handle = None
        file_pw = None
        if file.exists():
           file_handle, file_pw =  self._parse_config_file(file)
        if handle is None:
            if file_handle is None:
                raise ValueError('A bsky-handle was needed, but none was provided.')
            handle = file_handle
        if password is None:
            if file_pw is None:
                raise ValueError('An app password is needed, but none was provided')
            password = file_pw
        self.handle = handle
        self.client = Client()
        self.resolver = IdResolver()
        self.client.login(handle, password)

    @staticmethod
    def _parse_config_file(file: Path):
        config = ConfigParser()
        with open(file, 'r', encoding='utf-8') as f:
            config.read_string("[top]\n" + f.read())
        handle, password = None, None
        try:
            handle = config.get('top', 'my_handle')
            password = config.get('top', 'app_password')
        except NoOptionError:
            pass
        return handle, password


    def add_file_to_list(self, listname: str, file: Union[Path, str]) -> None:
        if file is not Path:
            file = Path(file)
        if not file.exists():
            raise FileNotFoundError(f'File {file} could not be found.')
        uri = self._get_list_uri(listname, self.handle)
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    line = line.rstrip()
                    if line.startswith('@'):
                        line = line[1::]
                    if not line.startswith('did:'):
                        line = self.resolver.handle.resolve(line)
                    self.client.app.bsky.graph.listitem.create(
                        self.handle,
                        models.AppBskyGraphListitem.Record(
                            list=uri,
                            subject=line,
                            created_at=self.client.get_current_time_iso()
                        )
                    )

    def backup_list(self, listname: str, owner: str, file: Path):
        uri = self._get_list_uri(listname, owner)
        cursor = None
        with open(file, 'w', encoding='utf-8') as f:
            while True:
                bskylist = self.client.app.bsky.graph.get_list(
                    models.AppBskyGraphGetList.Params(list=uri, limit=100, cursor=cursor)
                )
                cursor = bskylist.cursor
                for entry in bskylist.items:
                    f.write(entry.subject.did + '\n')
                if cursor is None:
                    break


    def _get_list_uri(self, listname: str, owner: str) -> str:
        response = self.client.app.bsky.graph.get_lists(
            models.AppBskyGraphGetLists.Params(
                actor=owner))
        for l in response.lists:
            if l['name'] == listname:
                uri = l['uri']
                break
        else:
            raise ListNotFoundException(f'List with name {listname} could not be found.')
        return uri






if __name__ == "__main__":
    from argparse import ArgumentParser
    p = ArgumentParser()
    subp = p.add_subparsers(dest='main_menu', required=True)
    list_parser = subp.add_parser('list')
    list_subp = list_parser.add_subparsers(dest='operation', required=True)
    add_p = list_subp.add_parser('add')
    add_p.add_argument('target_list_name')
    add_p.add_argument('file')
    download_p = list_subp.add_parser('download')
    download_p.add_argument('owner')
    download_p.add_argument('list_name')
    download_p.add_argument('file')
    args = p.parse_args()
    tool = BskyListTool(file='./config')
    match args.main_menu:
        case 'list':
            match args.operation:
                case 'add':
                    tool.add_file_to_list(args.target_list_name, args.file)
                case 'download':
                    tool.backup_list(args.list_name, args.owner, args.file)
