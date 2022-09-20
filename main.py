from flask import Flask, request
import flask
import json
from Blockchain import Blockchain
app = Flask(__name__)


blockchain = Blockchain()


@app.route("/")
def home():
    show_blocks = blockchain.show_blocks()
    return flask.jsonify({
        "message": "Blockchain with PoA",
        "Blockchain": show_blocks
    })

# validators get permission to join the network from project Leadership team
# by submitting required documents.


@app.route("/register/validator", methods=['POST'])
def register_validator():
    # payload should have country_id key
    payload = request.get_json(force=True)
    if not payload['country_id']:
        return flask.jsonify({
            "message": "validator country_id is missing ...."
        })
    blockchain.add_validator(payload)
    return flask.jsonify({
        "message": "validator added successfully.."
    })


@app.route("/register/peer", methods=["POST"])
def register_peer():
    # payload should contain public_key and amount
    payload = request.get_json(force=True)
    if not payload['public_key'] or not payload['amount']:
        return flask.jsonify({
            "message": "peer public key is missing ...."
        })
    blockchain.add_peer(payload)
    return flask.jsonify({
        "message": "peer added successfully.."
    })


@app.route("/view_all_peers")
def view_all_peers():
    peers = blockchain.view_all_peers()
    return flask.jsonify({
        "peers": peers
    })


@app.route("/view_all_validators")
def view_all_validators():
    validators = blockchain.view_all_validators()
    return flask.jsonify({
        "validators": validators
    })


@app.route("/view_transaction_pool")
def view_transaction_pool():
    transaction_pool = blockchain.view_all_transactions()
    return flask.jsonify({
        "transaction_pool": transaction_pool
    })


@app.route("/add_transaction/", methods=['POST'])
def add_transaction():
    # transaction should contain sender public key , receiver public key and amount
    transaction = request.get_json(force=True)
    if not transaction['sender'] or not transaction['receiver'] or not transaction['amount']:
        return flask.jsonify({
            "message": "Transaction format invalid...transaction should contain sender public key , receiver public key and amount.."
        })
    blockchain.add_transaction(transaction)
    return flask.jsonify({
        "message": "transaction added successfully."
    })

# validate transactions and add new blocks


@app.route("/mine")
def mine():
    if not blockchain.mine():
        return flask.jsonify({
            "message": "No Validators ...."
        })
    return flask.jsonify({
        "message": "mining successfull."
    })


if __name__ == '__main__':
    app.run(host="127.0.0.1", port="5000")
