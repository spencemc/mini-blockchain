import json
import requests
from proof_of_work import validate_blockchain_simple_pow
from block import Block

# Basic consensus algorithm which chooses the longest valid blockchain
def consensus(peer_nodes, node_blockchain):
	longest_chain = node_blockchain
	for chain in find_new_chains(peer_nodes):
		if len(longest_chain) < len(chain) and validate_blockchain_simple_pow(chain):
			longest_chain = chain
	if len(longest_chain) > len(node_blockchain):
		return update_blockchain(longest_chain)
	else:
		return node_blockchain

# Get blockchains of every other node
def find_new_chains(peer_nodes):
	other_chains = []
	for node_url in peer_nodes:
		chain = requests.get(node_url + "/blocks").json()
		for i in range(len(chain)):
			chain[i]['data'] = json.loads(chain[i]['data'])
		other_chains.append(chain)
	return other_chains

# Update the stored blockchain from the given json-formatted blockchain
def update_blockchain(chain):
	new_blockchain = []
	for b in chain:
		new_blockchain.append(Block(b['index'], b['timestamp'], b['data'], b['hash']))
	return new_blockchain