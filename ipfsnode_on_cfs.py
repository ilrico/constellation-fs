from apscheduler.schedulers.blocking import BlockingScheduler
import datetime as dt
import json
import sys

import ipfsapi
from constellationfs.ipfsnode import IPFSNode

ipfs = ipfsapi.connect('127.0.0.1', 5001)

FILE = 'constellationfs_ipfsnode.cfg'

def main(action):
    with open(FILE, 'r') as fh:
            config = json.loads(fh.read())
    if not config.get('IPFS_ADDRESS'):
        print('Node IPFS address is missing in config file')
    elif not config.get('CFS_PASSWORD'):
        print('Regarding the CFS password set in config file, you may do better...')
    elif not config.get('STELLAR_ADDRESS'):
        print('Node Stellar address is missing in config file')
    else:
        print("Starting...")
        node = IPFSNode()
        print("...config loaded:")
        print(f"IPFS address: {node.ipfs_address}\n" \
              f"Stellar address: {node.stellar_address}\n" \
              f"Scan bids every {node.book_scan_interval} minutes\n" \
              f"Place an offer on bids above {node.offer_limit} stroops/MB/day\n" \
              f"File maximum size is {node.size_mb_max} MB, maximum guaranteed pinning period is {node.days_max} days")
        if action == 'register':
            print(node.create().msg)
        if action == 'start':
            check = node.check()
            print(check.msg)
            if check.ok:
                main_loop(node)

def do_tasks(node):
    node.hit_bids(verbose=True)
    accepted_files = node.accept_deals()
    for file_hash in accepted_files:
        ipfs.pin_add(file_hash)
        print("{} has been pinned!".format(file_hash))

def main_loop(node):
    aps = BlockingScheduler()
    aps.add_job(do_tasks, 'interval', [node], minutes=node.book_scan_interval)
    print("...loop has been started (Ctrl-C to stop)")
    aps.start()

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] in ['register', 'start']:
        main(sys.argv[1])
    else:
        print('usage:\n'
              '  python ipfsnode_on_cfs.py <action>\n'
              'with <action> as\n'
              '  \'register\' to register an IPFS node on CFS\n'
              '  \'start\' to start CFS (Ctrl-C to stop)\n')