import getpass
import json

import click
from web3.auto import w3

from .transaction import CustomTransaction, HexBytes


@click.command()
@click.argument('keyfile', type=click.File())
@click.option('--payload', type=click.File(mode='rb'), default='-', show_default=True)
@click.option('--password', '-p')
def main(payload, keyfile, password):
    """
    Sign the `payload` (defaults to STDIN) using private key contained on `keyfile`
    decriptable with `password`.

    `password` will be prompted on tty if not provided via --password option
    """
    private_key: HexBytes = web3.eth.account.decrypt(keyfile.read(), password or getpass.getpass())
    transaction = CustomTransaction(data_body=payload.read())
    signed = transaction.sign(private_key)
    click.echo(json.dumps(signed.payload))


if __name__ == '__main__':
    main(prog_name='python -m polyswarmtransaction')
