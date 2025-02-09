from unittest.mock import patch

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from .models import Transaction


class FaucetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"

        cache.clear()

    def tearDown(self):
        # Clean up after each test
        cache.clear()
        Transaction.objects.all().delete()

    @patch("api.views.check_rate_limit")
    @patch("api.views.send_eth")
    def test_successful_fund_request(self, mock_send_eth, mock_rate_limit):
        # Configure mocks
        mock_rate_limit.return_value = True
        mock_send_eth.return_value = (
            "0xe9b7c78a15757af6c5af9bda165fc680be88039686296905a6f32c3aa070907d"
        )

        response = self.client.post(
            reverse("fund"), {"wallet_address": self.valid_address}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("transaction_id", response.data)
        self.assertEqual(
            response.data["transaction_id"],
            "0xe9b7c78a15757af6c5af9bda165fc680be88039686296905a6f32c3aa070907d",
        )

        # Verify that a transaction was created
        transaction = Transaction.objects.last()
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.status, "SUCCESS")
        self.assertEqual(transaction.wallet_address, self.valid_address)

    def test_invalid_address(self):
        response = self.client.post(
            reverse("fund"), {"wallet_address": "invalid"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rate_limit(self):
        with patch("api.utils.send_eth") as mock_send_eth:
            mock_send_eth.return_value = "0x123"

            # First request should succeed
            response1 = self.client.post(
                reverse("fund"), {"wallet_address": self.valid_address}, format="json"
            )

            # Second request should fail due to rate limit
            response2 = self.client.post(
                reverse("fund"), {"wallet_address": self.valid_address}, format="json"
            )

            self.assertEqual(response1.status_code, status.HTTP_200_OK)
            self.assertEqual(response2.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_stats_endpoint(self):
        # Create some test transactions
        now = timezone.now()
        Transaction.objects.create(
            wallet_address=self.valid_address,
            transaction_hash="0x123",
            amount=0.0001,
            status="SUCCESS",
            ip_address="127.0.0.1",
            created_at=now,
        )
        Transaction.objects.create(
            wallet_address=self.valid_address,
            transaction_hash=None,
            amount=0.0001,
            status="FAILED",
            ip_address="127.0.0.1",
            created_at=now,
        )

        response = self.client.get(reverse("stats"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["successful_transactions"], 1)
        self.assertEqual(response.data["failed_transactions"], 1)
