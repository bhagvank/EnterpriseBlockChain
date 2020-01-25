import hashlib as hasher
import datetime as date
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from collections import OrderedDict
import binascii
from urllib.parse import urlparse
from uuid import uuid4
import requests

class BlockChain:


    def __init__(self,Name):
        self.name = Name
        self.chain = []
        self.transactions_list = []
        self.nodes = set()
        self.node_id = str(uuid4()).replace('-', '')
        
    def append(self,block):
        self.chain.append(block) 
    
    def getTransactions(self):
        return self.transactions_list
        
    def next_block(self,Name,last_block):
        this_index = last_block.index + 1
        this_timestamp = date.datetime.now()
        this_data = Name + str(this_index)
        this_hash = last_block.hash
        block = Block(Name,this_index, this_timestamp, this_data, this_hash,self.transactions_list)
        self.transactions = []
        return block
    
    def pow(self):
        
        last_item = self.chain[-1]
        last_block_hash = last_item.hash_block()

        nonce_value = 0
        while self.check_pow_validity(self.transactions_list, last_block_hash, nonce_value) is False:
            nonce_value += 1

        return nonce_value
    
    def check_pow_validity(self, transactions_list, last_block_hash, nonce_value, difficulty=2):
        guess_value = (str(transactions_list)+str(last_block_hash)+str(nonce_value)).encode()
        guess_hash_value = hasher.sha256(guess_value).hexdigest()
        return guess_hash_value[:difficulty] == '0'*difficulty
    
    def add_transaction(self,transaction):
        self.transactions_list.append(transaction)
        
    def check_transaction_signature(self, sender_address, signature, transaction):
        
        public_key = RSA.importKey(binascii.unhexlify(sender_address))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA.new(str(transaction).encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(signature))


    def submit_transaction_after_verification(self, sender_address, recipient_address, value, signature):
        
        transaction = OrderedDict({'sender_address': sender_address, 
                                    'recipient_address': recipient_address,
                                    'value': value})

        #Reward for mining a block
        if sender_address == "THE BLOCKCHAIN":
            self.add_transaction(transaction)
            return len(self.chain) + 1
        else:
            transaction_verification = self.check_transaction_signature(sender_address, signature, transaction)
            if transaction_verification:
                self.add_transactions(transaction)
                return len(self.chain) + 1
            else:
                return False
    def add_node(self, node_url):
        parsed_url = urlparse(node_url)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')            
            
    def check_conflicts(self):
       
        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)


        for node in neighbours:
            print('http://' + node + '/chain')
            response = requests.get('http://' + node + '/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False        
        
        
class Block:        
        
    def __init__(self,Name,index, timestamp, data, previous_hash,transactions):
        self.name = Name
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()
        self.transactions = transactions

    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.index).encode('utf-8') + str(self.timestamp).encode('utf-8') + str(self.data).encode('utf-8') + str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()
    
    
        

blockchain = BlockChain("Enterprise BlockChain")

blockchain.submit_transaction_after_verification("THE BLOCKCHAIN","asdfasdlasd",400,"23423dasd") 

block = Block("Block1",0, date.datetime.now(), "Block1".encode('utf-8'), "0".encode('utf-8'),blockchain.getTransactions());
print(blockchain.name);

previous_block = block

num_of_blocks = 30


for i in range(0, num_of_blocks):
  blockchain.submit_transaction_after_verification("THE BLOCKCHAIN","asdfsdf",200+i,"23423dasd")    
  block_to_add = blockchain.next_block("num"+str(i),previous_block)
  blockchain.append(block_to_add)
  previous_block = block_to_add
  print("Block #{} is added to the blockchain!".format(block_to_add.index))
  print("Hash: {}\n".format(block_to_add.hash))

nonce_val = blockchain.pow()
print(nonce_val)

blockchain.add_node("http://node1")

blockchain.add_node("http://node2")

blockchain.add_node("http://node3")

blockchain.check_conflicts()





