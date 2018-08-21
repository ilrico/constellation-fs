# Constellation-FS

## Introduction
**IPFS** [[ipfs.io](https://ipfs.io)] is a distributed file storage system. Stable, fast and easy to use, IPFS is a very promising system to store data in a distributed way.

**Stellar**[[stellar.org](https://www.stellar.org)] is a decentralized payment system. It offers the best speed/cost ratio currently available. Transaction cost is virtually zero and validation time is around 5 seconds. Stellar is run by the Stellar Development Foundation, a non-profit organization.

**Constellation-FS** takes these two mature systems closer to fill a slight issue with IPFS: a file is dependant on its origin node uptime, except if it has been pinned (ie copied and set outside garbage collector scope) by other nodes. 

**Constellation-FS is an incentivation system for IPFS nodes to pin specific files, using the power of Stellar as micropayment infrastructure.**


## Principle
Constellation-FS (CFS) allows people to advertise their need to have their files pinned on IPFS. IPFS node owners can pin those files and get a financial compensation.
In practice it works like any market : people place bids, node owners reply with offers, a routine matches bids and offers. There is also a check that files are indeed pinned, etc...
CFS has mainly two kind of actors : *gateways* and *IPFS nodes*.

**Gateway**

A gateway allows its user to place bids for a particuliar file on the IPFS network. For this purpose, a gateway usually offers two functionalities : users can store a limited amount of *Lumens* (XLM) in a wallet, and they can upload their files to the IPFS network.

**IPFS Node**

An IPFS Node is just a normal IPFS node with CFS installed. Once its owner preferences are set, CFS will scan open bids, place offers in front, check if its offers are filled and pin the specific file if so. Everyone with some bandwith and storage available can run an IPFS Node with CFS.

**Bid**

A bid posted on CFS has mainly 3 properties: the bid limit (in *stroops*/MB/day), the minimum guaranteed days a file has to be pinned by one node, and the maximum nodes number requested. A *stroop* (STR) is 1 / 10 000 000 XLM. Currently mininum parameters for a bid are : 10 days, 1 MB. So if a user bids 82 requesting 3 nodes to pin his/her file, the wallet must hold 82 x 10 x 3 = 2460 STR + transactions fees (around 100 STR).

**Offer**

An offer will occur at bid price if the IPFS Node owner's preferences are compatible : bid price is above offer limit, file size is under IPFS Node maximum file size allowed and the minimum days requested is under IPFS Node maximum days.

**Matching**

After a bid is posted, a certain amount of time is left for offers to be placed. Then the origin gateway will match offers and bids.
Basically if there is less offers reply than requested pinning nodes for a given bid, all offers are filled, otherwise offers are filled randomly, remaining offers being on hold.

**Checking**

Once an offer is filled, it is expected that the IPFS Node pins the file. Gateways check at regular intervals that files are indeed still pinned by IPFS Node in the deal. If no downtime has occured, payment to IPFS Nodes are processed via Stellar. If a downtime has occured, then the deal is broken and the gateways looks to match another offer.


## Documentation


**Gateways**

Anyone can run a gateway. We'll soon open source code to setup a turn-key gateway.  
But most users will only want to use services offered by a gateway: upload a file on IPFS without running a node, and make sure this file is pinned.  
Today https://intrastellar.io offers this service. Users just have to create an account and credit a least XLM 1 on their wallet (it's a Stellar structural rule: wallets are only activated if they receive XLM 1).  
Once the wallet is activated, users can upload files and bids are automatically posted according to their settings.  

If you want to setup your gateway, you will need to pip install constellationfs and use the Gateway methods.


**IPFS node owner**

1. install the dependency, the beautiful Requests lib, the IPFS python wrapper, then constellationfs itself:  
    pip install requests  
    pip install ipfsapi  
    pip install constallationfs  
2. get the "daemon-like" helper  
    wget https://github.com/ilrico/constellation-fs/master/ipfsnode_on_cfs.py  
3. get the config file template  
    wget https://github.com/ilrico/constellation-fs/master/constellationfs_ipfsnode_template.cfg  
4. edit the config file (basically, add your IPFS address, a password and your Stellar wallet address  
5. rename the config file to constellationfs_ipfsnode.cfg  
6. run the ipfsnode_on_cfs.py (better with tmux)  


