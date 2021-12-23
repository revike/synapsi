import hashlib
import requests


class SessionAPI:
    """Session synapsi.xyz"""

    def __init__(self, base_url, login, password, headers):
        self.base_url = base_url
        self.login = login
        self.password = password
        self.headers = headers
        self.session = requests.Session()
        self.session.auth = (self.login, self.get_hash_password())

    def get_hash_password(self):
        """Get hash_password md5"""
        password_md5 = hashlib.md5(self.password.encode('utf-8'))
        password_hash = password_md5.hexdigest()
        return password_hash

    def get_data(self):
        """Get data API"""
        data = self.session.get(
            f'{self.base_url}dataset', headers=self.headers).json()
        return data

    def post_answer(self, answer):
        """POST answer"""
        response = self.session.post(f'{self.base_url}answers',
                                     headers=self.headers, json=answer)
        return response

    def post_file(self):
        """POST file"""
        files = {'file': ('file.txt', open('file.txt', 'rb'), 'text/txt')}
        response = self.session.post(f'{self.base_url}code', files=files,
                                     headers=self.headers)
        return response

    def put_mark(self):
        """Mark the completion of the task"""
        return self.session.put(f'{self.base_url}done', headers=self.headers)
