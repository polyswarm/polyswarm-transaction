# polyswarm-transaction
Transaction module for building, signing, and verifying transactions for the db backed sidechain

## Transactions

### Structure

```json
{
    "name": "<module>:<class>",
    "from": "<public key checksum address>",
    "data": {}
}
```

Transactions are made of three parts; name, from, and data

The name defines which transaction is being called.
The server side is able to use that and verify that it can perform the requested transaction.

The from field is an ethereum address that tells us who sent the message.
This address is confirmed with the signature so we can be absolutely certain who sent the transaction.

The data field is the arguments that are passed to the named Transaction.


### Signatures

To remain compatible with existing ERC20 tokens, the signature scheme makes heavy use of existing web3 tools.
The keys are all ethereum public-private secp256k1 keypairs, and it uses keccak as the hash function.

When we prepare for signing, we output the python dictionaries as a json string, and keep that string stored.
This string allows us to ensure order is maintained in transit, which cannot be done when json is loaded.
The string is then hashed with keccak, and the user's private key can sign the hashed message.


## Use

The primary use case of this library is to define the protocol by which transactions are transmitted.
By simply overriding `Transaction` one can build any transactions that will easily conform to the standard.

By default the following transactions are already defined.

1. `bounty.BountyTransaction`
1. `bounty.AssertionTransaction`
1. `bounty.VoteTransaction`
1. `nectar.WithdrawalTransaction`

Is also defined a `transaction.CustomTransaction` accepting a `data_body`
that you may handcraft for testing purposes.

Using the `sign()` method, these transactions will be transformed into a json string and signature.
This signature can be verified the `ecrecover` method on `SignedTransaction`


### Build Transactions

```python
import requests

from web3.auto import w3
from polyswarmtransaction.bounty import BountyTransaction

demo_account = w3.eth.account.from_key([0] * 32)


transaction = BountyTransaction(guid, reward, artifact, artifact_type, metadata, duration)
signed = transaction.sign(demo_account.key)

# Send as form data so server doesn't load json string
response = requests.post(server_url, data=signed.payload)
response.raise_for_status()
```


### Verify Signed Transactions

```python
from polyswarmtransaction import SignedTransaction
from polyswarmtransaction.bounty import BountyTransaction
from django.http import HttpResponse

def bounty_view():
    data = request.POST.dict()
    signed = SignedTransaction(**data)
    
    # Public key is verified during recovery
    address = signed.ecrecover()
    try:
        bounty_transaction = signed.transaction()
    except (UnsupportedTransactionError, ValueError, ValidationError, WrongSignatureError, InvalidSignatureError):
        return HttpResponse('', 400)

    if not isinstance(bounty_transaction, BountyTransaction):
        return HttpResponse('', 400)

    do_work(address, bounty_transaction)
```


### Signing payloads from CLI

For testing purposes is possible to sign arbitrary JSON payloads from commandline.
They will all be encapsulated on a CustomTransaction before signing.

Password should be provided via `-p/--password` or will be requested on /dev/tty

```console
$ python -m polyswarmtransaction /path/to/keyfile --payload path/to/payload.json -p mypassword
{"raw_transaction": "{\"name\": \"polyswarmtransaction.transaction:CustomTransaction\", \"from\": \"0x05328f171b8c1463eaFDACCA478D9EE6a1d923F8\", \"data\": ... \"}", "signature": "0x6ff71bfc58aa72bf4c8b0388c44d5151456a52eb1f1bc6f4825034cb96d0f2a90aa10afb3dd7aada15799bfb7a25f342e3e04ec02830807fde9222ad385ef6e700"}
```

You can also provide the JSON payload via STDIN:
```console
$ echo '"DEADBEEF"' | python -m polyswarmtransaction /path/to/keyfile -p mypassword
{"raw_transaction": "{\"name\": \"polyswarmtransaction.transaction:CustomTransaction\", \"from\": \"0x05328f171b8c1463eaFDACCA478D9EE6a1d923F8\", \"data\": \"DEADBEEF\"}", "signature": "0x182195b3f7734ff2bb54545f29c3a961885c95bed4b989d7e9866dacd07090f258cffe8b9e39fb97435cd10d0f4131e7de59b76fce3ce7e3aa70874da39c949600"}
```
