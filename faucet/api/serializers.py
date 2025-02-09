from rest_framework import serializers

from .models import Transaction


class FundRequestSerializer(serializers.Serializer):
    wallet_address = serializers.RegexField(regex=r"^0x[a-fA-F0-9]{40}$", required=True)


class TransactionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["transaction_hash", "amount", "status", "created_at"]
