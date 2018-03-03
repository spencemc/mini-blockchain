# Simple proof of work:
# Increment last_proof until it is divisible by 9 and 
#   divisible by the previous proof of work
def do_simple_pow(last_proof):
	incrementor = last_proof + 1
	while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
		incrementor += 1
	return incrementor

# Validate the proof of work in the given blockchain
def validate_blockchain_simple_pow(chain):
	print(str(chain))
	for i in range(1, len(chain)):
		last_proof = chain[i - 1]['data']['proof-of-work']
		curr_proof = chain[i]['data']['proof-of-work']
		if not valid_simple_pow(curr_proof, last_proof):
			return False
	return True

# Check if the given proof of work is valid with respect to the last proof of work
def valid_simple_pow(proof, last_proof):
	return (proof > last_proof 
		and proof % 9 == 0 
		and proof % last_proof == 0)