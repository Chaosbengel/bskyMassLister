from atproto_client import Client, models
from atproto_client.exceptions import BadRequestError
from configparser import ConfigParser, NoOptionError
from pathlib import Path
from typing import Union, Iterable


class ListNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)


class BskyListTool:
    def __init__(self, handle: str=None, password: str=None, cred_file: Union[Path,str]=None,
                 token_file: Union[Path, str]=None):
        token = self._read_token_from_file(token_file)
        if cred_file is not Path:
            cred_file = Path(cred_file)
        file_handle = None
        file_pw = None
        if cred_file.exists():
           file_handle, file_pw =  self._parse_config_file(cred_file)
        if handle is None:
            if file_handle is None:
                raise ValueError('A bsky-handle was needed, but none was provided.')
            handle = file_handle
        if password is None:
            if file_pw is None:
                raise ValueError('An app password is needed, but none was provided')
            password = file_pw
        self.token_file = token_file
        self.handle = handle
        self.client = Client()
        if token is None:
            self.client.login(handle, password)
        else:
            self.client.login(session_string=token)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.save_token()

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

    def _link_to_at_uri(self, link: str) -> str:
        http_url = link.split('/')
        profile = http_url[4]
        rkey = http_url[6]
        did = self.client.resolve_handle(profile).did
        at_uri = f"at://{did}/app.bsky.feed.post/{rkey}"
        return at_uri

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

    @staticmethod
    def _read_token_from_file(file: Union[Path, str]) -> Union[str, None]:
        if file is not Path:
            file = Path(file)
        if file.exists():
            with open(file, 'r', encoding='utf-8') as f:
                token = f.read()
            return token
        else:
            return None

    def add_file_to_list(self, listname: str, file: Union[Path, str]):
        subjects = self.load_listfile(file)
        self.add_to_list(listname, subjects)

    def add_to_list(self, listname: str, subjects: Iterable[str]):
        uri = self._get_list_uri(listname, self.handle)
        for subject in subjects:
            if not subject.startswith('did:'):
                subject = self.client.resolve_handle(subject)
                self.client.app.bsky.graph.listitem.create(
                    self.handle,
                    models.AppBskyGraphListitem.Record(
                        list=uri,
                        subject=subject,
                        created_at=self.client.get_current_time_iso()
                    )
                )

    def fetch_list(self, listname: str, owner: str):
        uri = self._get_list_uri(listname, owner)
        cursor = None
        dids = []
        while True:
            bskylist = self.client.app.bsky.graph.get_list(
                models.AppBskyGraphGetList.Params(list=uri, limit=100, cursor=cursor)
            )
            cursor = bskylist.cursor
            for entry in bskylist.items:
                dids.append(entry.subject.did)
            if cursor is None:
                break
            return dids

    def fetch_followers(self, handle: str):
        cursor = None
        followers = []
        while True:
            followers = self.client.get_followers(actor=handle, limit=100, cursor=cursor)
            cursor = followers.cursor
            for follower in followers.followers:
                followers.append(follower.did)
            if cursor is None:
                break
        return followers

    def fetch_likes(self, post_url: str):
        at_uri = self._link_to_at_uri(post_url)
        cursor = None
        dids = []
        while True:
            response = self.client.get_likes(uri=at_uri, limit=100, cursor=cursor)
            cursor = response.cursor
            for like in response.likes:
                dids.append(like.actor.did)
            if cursor is None:
                break
        return dids

    def load_listfile(self, file: Union[Path, str]) -> list[str]:
        dids = []
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    line = line.rstrip()
                    if line.startswith('@'):
                        line = line[1::]
                    if not line.startswith('did:'):
                        try:
                            line = self.client.resolve_handle(line)
                        except BadRequestError as e:
                            if e.response.content.message == "Unable to resolve handle":
                                print(f"could not resolve handle {line}, skipping..")
                                continue
                            else:
                                raise
                    dids.append(line)
        return dids

    def save_token(self):
        token = self.client.export_session_string()
        with open(self.token_file, 'w', encoding='utf-8') as f:
            f.write(token)

    @staticmethod
    def write_to_file(collection: Iterable[str], file: Union[Path, str]):
        if file is not Path:
            file = Path(file)
            if file.exists():
                userinput = input(f"File {file} already exists. Do you want to overwrite? [Y|y]: ")
                userinput = userinput.lower()
                if not userinput.startswith('y'):
                    print("Nothing was written.")
                    return
                with open(file, 'w', encoding='utf-8') as f:
                    for elem in collection:
                        f.write(elem + '\n')
                print("Saved to disk.")
