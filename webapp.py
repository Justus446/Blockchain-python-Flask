import json
from flask import *
from Blockchain import Blockchain
from time import time


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
