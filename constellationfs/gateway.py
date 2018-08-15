import json
import requests

from .result import Result


class Gateway:

    def __init__(self, file='constellationfs_gateway.cfg'):
        with open(file, 'r') as fh:
            config = json.loads(fh.read())
        self.ipfs_address = config.get('IPFS_ADDRESS', '')
        self.admin_email = config.get('ADMIN_EMAIL', '')
        self.token = config.get('TOKEN', '')
        self.api_version = config.get('API_VERSION', 1)
        self.stellar_address = config.get('STELLAR_ADDRESS')

    def check(self):
        result = Result()
        url = 'https://constellation-fs.org/api/cfs/v{api_version}/gateway/check'.format(api_version=self.api_version)
        data = {'IPFS_ADDRESS': self.ipfs_address,
                'TOKEN': self.token}
        r = requests.post(url, data)
        if r.status_code == 200:
            result.load_from_dict(r.json())
        else:
            result.error_msg = f'[ERROR] {r.status_code}'
        return result.process()

    def create(self):
        result = Result()
        url = 'https://constellation-fs.org/api/cfs/v{api_version}/gateway/create'.format(api_version=self.api_version)
        data = {'IPFS_ADDRESS': self.ipfs_address,
                'ADMIN_EMAIL': self.admin_email}
        r = requests.post(url, data=data)
        if r.status_code == 200:
            result.load_from_dict(r.json())
        else:
            result.error_msg = f'[ERROR] {r.status_code}'
        return result.process()

    def place_bid(self, file_hash='', size_mb=0, days_min=10, bid_limit=0, nodes_max=3):
        result = Result()
        if file_hash and bid_limit:
            url = 'https://constellation-fs.org/api/cfs/v{api_version}/book/bid/add'.format(api_version=self.api_version)
            data = {'IPFS_ADDRESS': self.ipfs_address,
                    'TOKEN': self.token,
                    'FILE_HASH': file_hash,
                    'SIZE_MB': size_mb,
                    'BID_LIMIT': bid_limit}
            r = requests.post(url, data)
            if r.status_code == 200:
                result.load_from_dict(r.json())
        else:
            result.error_msg = f'[ERROR] {r.status_code}'
        return result.process()

    def match_offers(self):
        result = Result()
        url = 'https://constellation-fs.org/api/cfs/v{api_version}/book/offer/match'.format(api_version=self.api_version)
        data = {'IPFS_ADDRESS': self.ipfs_address,
                'TOKEN': self.token}
        r = requests.post(url, data)
        if r.status_code == 200:
            result.load_from_dict(r.json())
        else:
            result.error_msg = f'[ERROR] {r.status_code}'
        return result.process()

    def get_file_info(self, file_hash):
        result = Result()
        url = 'https://constellation-fs.org/api/cfs/v{api_version}/file/info'.format(api_version=self.api_version)
        data = {'IPFS_ADDRESS': self.ipfs_address,
                'TOKEN': self.token,
                'FILE_HASH': file_hash}
        r = requests.post(url, data)
        if r.status_code == 200:
            result.load_from_dict(r.json())
        else:
            result.error_msg = f'[ERROR] {r.status_code}'
        return result.process()