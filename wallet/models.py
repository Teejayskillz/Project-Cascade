import uuid
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from decimal import Decimal

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'), help_text="The user's current balance in NGN.")
    currency = models.CharField(max_length=10, default='NGN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Wallet - {self.balance} {self.currency}"

    def deposit(self, amount):
        if amount <= 0:
            raise ValidationError("Amount must be positive.")
        self.balance += Decimal(amount)
        self.save()

    def withdraw_funds(self, amount):
        if amount <= 0:
            raise ValidationError("Amount must be positive.")
        if amount > self.balance:
            raise ValidationError("Insufficient funds.")
        self.balance -= Decimal(amount)
        self.save()