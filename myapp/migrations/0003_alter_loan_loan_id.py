# Generated by Django 5.1.4 on 2025-03-03 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_loan_loan_id_alter_loan_monthly_installment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='loan_id',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
