import ipfsapi
import json
import requests

from .result import Result

ipfs = ipfsapi.connect('localhost', 5001)

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
                    'BID_LIMIT': bid_limit,
                    'DAYS_MIN': days_min,
                    'NODES_MAX': nodes_max}
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

    def load_pinned_objects(self):
        q = ipfs.pin_ls(type='recursive')
        if q:
            self.pinned_objects = list(q['Keys]'].keys())
        return self

    def force_deal(self, file_hash, price):
        result = Result()
        url = 'https://constellation-fs.org/api/cfs/v{api_version}/deal/force'.format(api_version=self.api_version)
        data = {'IPFS_ADDRESS': self.ipfs_address,
                'TOKEN': self.token,
                'STELLAR_ADDRESS': self.stellar_address,
                'FILE_HASH': file_hash,
                'DEAL_PRICE': price}
        r = requests.post(url, data)
        if r.status_code == 200:
            result.load_from_dict(r.json())
        else:
            result.error_msg = f'[ERROR] {r.status_code}'
        return result.process()
