# Generated by Django 5.1.6 on 2025-02-08 00:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_remove_transaction_api_transac_created_752f02_idx_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="transaction_hash",
            field=models.CharField(
                max_length=66,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(regex="^0x[A-Fa-f0-9]{64}$")
                ],
                verbose_name="Ethereum Transaction hash",
            ),
        ),
    ]
