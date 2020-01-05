import hashlib as hasher
import datetime as date

class BlockChain:


    def __init__(self,Name):
        self.name = Name
        self.chain = []
        self.transactions_list = []
        
    def append(self,block):
        self.chain.append(block) 
    
    def next_block(self,Name,last_block):
        this_index = last_block.index + 1
        this_timestamp = date.datetime.now()
        this_data = Name + str(this_index)
        this_hash = last_block.hash
        return Block(Name,this_index, this_timestamp, this_data, this_hash) 
    
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
        
        
class Block:        
        
    def __init__(self,Name,index, timestamp, data, previous_hash):
        self.name = Name
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.index).encode('utf-8') + str(self.timestamp).encode('utf-8') + str(self.data).encode('utf-8') + str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()
    
    
        

blockchain = BlockChain("Enterprise BlockChain")

block = Block("Block1",0, date.datetime.now(), "Block1".encode('utf-8'), "0".encode('utf-8'));
print(blockchain.name);

previous_block = block

num_of_blocks = 30


for i in range(0, num_of_blocks):
  block_to_add = blockchain.next_block("num"+str(i),previous_block)
  blockchain.append(block_to_add)
  previous_block = block_to_add
  print("Block #{} is added to the blockchain!".format(block_to_add.index))
  print("Hash: {}\n".format(block_to_add.hash))

nonce_val = blockchain.pow()
print(nonce_val)






