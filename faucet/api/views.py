import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Transaction
from .serializers import FundRequestSerializer
from .utils import check_rate_limit, get_24h_stats, send_eth, set_rate_limit

logger = logging.getLogger(__name__)


class FundView(APIView):
    def post(self, request):
        serializer = FundRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        wallet_address = serializer.validated_data["wallet_address"]
        ip_address = request.META.get("REMOTE_ADDR")

        if not check_rate_limit(wallet_address, ip_address):
            return Response(
                {"error": "Rate limit exceeded. Please try again in X seconds"},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        try:
            tx_hash = send_eth(wallet_address)
            Transaction.objects.create(
                wallet_address=wallet_address,
                transaction_hash=tx_hash,
                amount=0.0001,
                status="SUCCESS",
                ip_address=ip_address,
            )
            return Response(
                {
                    "transaction_id": tx_hash,
                    "message": "Successfully sent 0.0001 Sepolia ETH",
                }
            )
        except Exception as e:
            logger.error(f"Transaction failed: {str(e)}")
            Transaction.objects.create(
                wallet_address=wallet_address,
                transaction_hash="",
                amount=0.0001,
                status="FAILED",
                ip_address=ip_address,
            )
            return Response(
                {"error": f"Transaction failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        finally:
            set_rate_limit(wallet_address, ip_address)


class StatsView(APIView):
    def get(self, request):
        return Response(get_24h_stats())
