from time import time
from hashlib import sha256
import json
from flask import *


class Block:

    def __init__(self, index, prev_hash, data, timestamp):
        self.index = index
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    difficulty = 5

    def __init__(self):

        self.genesis_block = self.gen_block()
        self.chain = [self.genesis_block]
        self.unconfirmed_transactions = []

    def gen_block(self):
        g_block = Block(0, 0, "this is Kakamega", time())
        return g_block

    # @property
    def last_block(self):
        return self.chain[-1]

    # DONE :used to look for the nonce that produces the number of zeroes and return tits hash
    def proof_of_work(self, block):
        block.nonce = 0
        data = block.compute_hash()
        while not str(data).startswith("0" * self.difficulty):
            print(data)
            block.nonce += 1
            data = (str(data) + str(block.nonce))
            data = sha256(data.encode()).hexdigest()

        return data

    # DONE : checks if block starts withe THE number of zeros and its hash is correct
    @staticmethod
    def isvalid_proof(block, block_hash):
        return (block_hash.startswith("0" * Blockchain.difficulty) and block_hash == block.compute_hash()
                )

    def add_block(self, block, proof):
        prev_hash = self.last_block.compute_hash()

        if prev_hash != block.prev_hash and not Blockchain.isvalid_proof(block, block.compute_hash()):
            return False
        else:
            block.hash = proof
            self.chain.append(block)
            return True

    # DONE : this adds new transactions to the list of unconfirmed transactions
    def add_new_block(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    #  DONE : adds pending transaction to the blockchain, transaction is added to a new block and POW figured out
    def mine(self):

        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block()

        new_block = Block(index=last_block.index + 1, prev_hash=last_block.hasher, data=self.unconfirmed_transactions,
                          timestamp=time())

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index


"""""
b = Block(1, 6, 5, 1234)

b1 = Blockchain()
print(b.compute_hash())

print("computing last block")
print(b1.proof_of_work(b))
print("work done") """

"""WORK ON FLASK BEGINS HERE


"""
blockchain1 = Blockchain()

app = Flask(__name__)

app.secret_key = 'hello'


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/account')
def account():
    return render_template('login.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/table/')
def table():
    return render_template('table.html')


@app.route('/verify/', methods=['POST'])
def verify():
    data = request.form['title']
    chain = blockchain1.chain
    for x in chain:
        if x.data == data:
            return render_template('login.html')
        else:
            flash("title not found")
            return redirect(url_for(index))


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        flash("sign up successful")
    else:
        return redirect(url_for('/'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.form['username'] and request.form['password'] == 'admin':
        return render_template('transaction.html')
        # return redirect(url_for(new_transaction))

    else:
        flash("login successful")
        return render_template('table.html')


@app.route('/logout/', )
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


# @app.route('/<profile>/')
# def profile_page(profile):
# return f"<h1>{profile}<h1>"


@app.route('/transact/', )
def transact():
    return render_template('transaction.html')


# okay...where user transfers land to another, it is a form
@app.route('/new_transaction/', methods=['POST', 'GET'])
def new_transaction():
    input_data = []
    if request.method == 'POST':
        input_data = [request.form['title'], request.form['buyerid'], request.form['sellerid'], time.time()]
        blockchain1.add_new_block(input_data)
        flash("transaction successful")
    else:
        flash("Transaction unsuccessful")
        render_template('login.html')

    return "success", 201


# returns the entire blockchain
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain1.chain:
        chain_data.append(block.__dict__)

    return json.dumps(chain_data)


@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    result = blockchain1.mine()
    if not result:
        return "No transaction to mine"
    return "Block #{} is mined".format(result)


@app.route('/pending Data')
def get_pending_data():
    return json.dumps(blockchain1.unconfirmed_transactions)


if __name__ == '__main__':
    app.run(debug=True)
