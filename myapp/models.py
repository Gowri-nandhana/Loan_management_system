import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')


# Loan Model
class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_id = models.CharField(max_length=10, unique=True, blank=True, null=True)  # Allow blank & null
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()  # months
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # yearly
    total_interest = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Calculate EMI, total interest, and total amount before saving."""
        if not self.loan_id:  # Generate loan_id only if it's missing
            self.loan_id = f"LOAN{uuid.uuid4().hex[:6].upper()}"

        if self.amount and self.interest_rate and self.tenure:
            monthly_rate = self.interest_rate / 12 / 100
            emi = (self.amount * monthly_rate * ((1 + monthly_rate) ** self.tenure)) / (((1 + monthly_rate) ** self.tenure) - 1)
            total_interest = (emi * self.tenure) - self.amount

            self.total_interest = round(total_interest, 2)
            self.total_amount = round(self.amount + total_interest, 2)
            self.monthly_installment = round(emi, 2)

        super().save(*args, **kwargs)
