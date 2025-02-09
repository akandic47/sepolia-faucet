from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.core.cache import cache
from web3 import Web3


def get_web3():
    return Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URL))


def check_rate_limit(wallet_address, ip_address):
    wallet_key = f"rate_limit_wallet_{wallet_address}"
    ip_key = f"rate_limit_ip_{ip_address}"

    if cache.get(wallet_key) or cache.get(ip_key):
        return False

    return True


def set_rate_limit(wallet_address, ip_address):
    wallet_key = f"rate_limit_wallet_{wallet_address}"
    ip_key = f"rate_limit_ip_{ip_address}"

    cache.set(wallet_key, True, timeout=settings.RATE_LIMIT_MINUTES * 60)
    cache.set(ip_key, True, timeout=settings.RATE_LIMIT_MINUTES * 60)


def send_eth(to_address):
    web3 = get_web3()
    account = web3.eth.account.from_key(settings.SOURCE_WALLET_PRIVATE_KEY)

    transaction = {
        "nonce": web3.eth.get_transaction_count(account.address, "pending"),
        "to": to_address,
        "value": web3.to_wei(settings.ETH_AMOUNT, "ether"),
        "gas": 21000,
        "gasPrice": web3.eth.gas_price,
        "chainId": web3.eth.chain_id,
    }

    signed_txn = web3.eth.account.sign_transaction(transaction, account.key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    return web3.to_hex(tx_hash)


def get_24h_stats():
    from .models import Transaction

    time_threshold = datetime.now(timezone.utc) - timedelta(hours=24)
    success_count = Transaction.objects.filter(
        status="SUCCESS", created_at__gte=time_threshold
    ).count()

    failed_count = Transaction.objects.filter(
        status="FAILED", created_at__gte=time_threshold
    ).count()

    return {
        "successful_transactions": success_count,
        "failed_transactions": failed_count,
    }
