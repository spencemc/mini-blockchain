import json
from flask import Flask
from flask import request
from model import Model
node = Flask(__name__)
model = Model()

# Start the server on the given port
def start_server(port):
	node.run(port=port)

# Submit a transaction to the node.
@node.route('/tx', methods=['POST'])
def transaction():
	if request.method == 'POST':
		# Get the transaction data
		new_tx = request.get_json()

		# Add the transaction to this nodes list
		model.add_transaction(new_tx)

		# Log the transaction
		print("New transaction")
		print("FROM: {}".format(new_tx['from']))
		print("TO: {}".format(new_tx['to']))
		print("AMOUNT: {}".format(new_tx['amount']))

		return "Transactions submission successful\n"

# Mine a new block and add it to the blockchain
@node.route('/mine', methods=['GET'])
def mine():
	mined_block = model.mine()
	return json.dumps({
		"index" : mined_block.index,
		"timestamp" : str(mined_block.timestamp),
		"data" : mined_block.data,
		"hash" : mined_block.hash
		}) + "\n" 

# Get a list of blocks in the blockchain
@node.route('/blocks', methods=['GET'])
def get_blocks():
	return json.dumps(model.get_blocks())

# Sync the blockchain with peers
@node.route('/sync', methods=['GET'])
def sync_chain():
	model.sync_chain()
	return "Chain is now synced with all peers.\n"

# Add a peer to watch
@node.route('/add_peer', methods=['POST'])
def add_peer():
	if request.method == 'POST':
		new_peer = request.get_json()
		model.add_peer(new_peer['url'])
		return "Peer successfully added\n"