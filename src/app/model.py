import json
import datetime as date
from utils.block import Block
from utils.consensus import consensus
from utils.proof_of_work import do_simple_pow

# Create a genesis block to start the blockchain
# Genesis block has to have an index of 0 and can have any previous hash.
def create_genesis_block():
	return Block(0, date.datetime.now(), { 
		"proof-of-work" : 9,
		"transactions"  : None
		}, "0")

class Model:
	def __init__(self):
		# Transactions stored in the node
		self.transactions = []
		# Random miner address
		self.miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"
		# Local copy of the blockchain
		self.blockchain = [create_genesis_block()]
		# Other peers that are connected
		self.peer_nodes = []

	def add_transaction(self, tx):
		self.transactions.append(tx)

	def add_peer(self, peer_url):
		self.peer_nodes.append(peer_url)

	def sync_chain(self):
		self.blockchain = consensus(self.peer_nodes, self.blockchain)

	def mine(self):
		last_block = self.blockchain[len(self.blockchain) - 1]
		last_proof = last_block.data['proof-of-work']
		proof = do_simple_pow(last_proof)
		self.transactions.append(
			{ "from" : "network", "to" : self.miner_address, "amount" : 1 }
		)
		new_block_data = {
			"proof-of-work" : proof,
			"transactions" : list(self.transactions)
		}
		new_block_index = last_block.index + 1
		new_block_timestamp = date.datetime.now()
		last_block_hash = last_block.hash

		# Empty the transaction list
		self.transactions[:] = []

		# Create new block
		mined_block = Block(new_block_index, new_block_timestamp, new_block_data, last_block_hash)
		self.blockchain.append(mined_block)
		
		return mined_block

	def get_blocks(self):
		blocks = []
		for block in self.blockchain:
			blocks.append({
				"index" : str(block.index),
				"timestamp" : str(block.timestamp),
				"data" : json.dumps(block.data),
				"hash" : block.hash
			})
		return blocks