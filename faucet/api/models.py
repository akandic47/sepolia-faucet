from django.core.validators import RegexValidator
from django.db import models


class Transaction(models.Model):
    wallet_address = models.CharField(
        max_length=42,
        verbose_name="Ethereum Wallet Address",
        validators=[RegexValidator(regex=r"^0x[a-fA-F0-9]{40}$")],
    )
    transaction_hash = models.CharField(
        max_length=66,
        verbose_name="Ethereum Transaction hash",
        validators=[RegexValidator(regex=r"^0x[A-Fa-f0-9]{64}$")],
        null=True,
    )
    # We will leave this commented for the sake of simplicity and testability
    # nonce = models.IntegerField(
    #    verbose_name="Transaction nonce",
    #    null=False
    # )
    amount = models.DecimalField(
        max_digits=18, verbose_name="Amount of ETH being sent", decimal_places=8
    )
    status = models.CharField(
        max_length=7, choices=[("SUCCESS", "Success"), ("FAILED", "Failed")]
    )
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["wallet_address"]),
            models.Index(fields=["transaction_hash"]),
        ]
