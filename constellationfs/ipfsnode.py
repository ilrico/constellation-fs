import hashlib
import json
import requests

from .result import Result


class IPFSNode:

    def __init__(self, file='constellationfs_ipfsnode.cfg'):
        with open(file, 'r') as fh:
            config = json.loads(fh.read())
        self.ipfs_address = config.get('IPFS_ADDRESS', '')
        self.cfs_password = hashlib.sha3_256(config.get('CFS_PASSWORD', '').encode('ascii')).hexdigest()
        self.api_version = config.get('API_VERSION', 1)
        self.stellar_address = config.get('STELLAR_ADDRESS')
        self.book_scan_interval = int(config.get('BOOK_SCAN_INTERVAL', 10))
        self.offer_limit = int(config.get('OFFER_LIMIT', 10000000))
        self.size_mb_max = int(config.get('FILESIZE_MB_MAX', 10000000))
        self.days_max = int(config.get('DAYS_MAX', 10))

    def check(self):
        result = Result()
        url = 'https://constellation-fs.org/api/cfs/v{api_version}/ipfsnode/check'.format(api_version=self.api_version)
        data = {'IPFS_ADDRESS': self.ipfs_address,
                'PWD': self.cfs_password}
        r = requests.post(url, data)
        if r.status_code == 200:
            result.load_from_dict(r.json())
        else:
            result.error_msg = '[ERROR] IPFSNode check failed'
        return result.process()

    def create(self):
        result = Result()
        url = 'https://constellation-fs.org/api/cfs/v{api_version}/ipfsnode/create'.format(api_version=self.api_version)
        data = {'IPFS_ADDRESS': self.ipfs_address,
                'PWD': self.cfs_password}
        r = requests.post(url, data=data)
        if r.status_code == 200:
            result.load_from_dict(r.json())
        else:
            result.error_msg = f'[ERROR] {r.status_code}'
        return result.process()

    def list_bids(self):
        result = Result()
        url = f'https://constellation-fs.org/api/cfs/v{self.api_version}/book/bids'
        data = {'IPFS_ADDRESS': self.ipfs_address,
                'PWD': self.cfs_password,
                'SIZE_MB_MAX': self.size_mb_max,
                'DAYS_MAX': self.days_max,
                'OFFER': self.offer_limit}
        r = requests.post(url, data=data)
        if r.status_code == 200:
            result.load_from_dict(r.json())
        else:
            result.error_msg = f'[ERROR] {r.status_code}'
        return result.process()

    def hit_bids(self, verbose=False):
        result = Result()
        r_list_bids = self.list_bids()
        if r_list_bids.ok:
            bid_counter = 0
            print(r_list_bids.data)
            bid_uuids = [bid['uuid'] for bid in r_list_bids.data]
            for bid_uuid in bid_uuids:
                r = self.place_offer(bid_uuid)
                if verbose:
                    print('  {}'.format(r.msg))
            result.success_msg = "{} offer(s) sent".format(bid_counter)
        else:
            result = r_list_bids
        return result.process()

    def place_offer(self, bid_uuid):
        result = Result()
        url = f'https://constellation-fs.org/api/cfs/v{self.api_version}/book/offer/add'
        data = {'IPFS_ADDRESS': self.ipfs_address,
                'PWD': self.cfs_password,
                'BID_UUID': bid_uuid,
                'SIZE_MB_MAX': self.size_mb_max,
                'DAYS_MAX': self.days_max,
                'OFFER': self.offer_limit}
        r = requests.post(url, data=data)
        if r.status_code == 200:
            result.load_from_dict(r.json())
        else:
            result.error_msg = f'[ERROR] {r.status_code}'
        return result.process()

    def accept_deals(self):
        result = Result()
        url = f'https://constellation-fs.org/api/cfs/v{self.api_version}/deal/accept'
        data = {'IPFS_ADDRESS': self.ipfs_address,
                'PWD': self.cfs_password,
                'STELLAR_ADDRESS': self.stellar_address}
        r = requests.post(url, data=data)
        if r.status_code == 200:
            result.load_from_dict(r.json())
        else:
            result.error_msg = f'[ERROR] {r.status_code}'
        return result.process()

    def declare_pin(self, file_hash):
        result = Result
        url = f'https://constellation-fs.org/api/cfs/v{self.api_version}/deal/pin/declare'
        data = {'IPFS_ADDRESS': self.ipfs_address,
                'PWD': self.cfs_password,
                'FILE_HASH': file_hash}
        r = requests.post(url, data=data)
        if r.status_code == 200:
            result.load_from_dict(r.json())
        else:
            result.error_msg = f'[ERROR] {r.status_code}'
        return result.process()

