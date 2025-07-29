import uuid
from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    """
    Represents an order made by a user (:model: `auth.User`)
    """
    DESIGN_TYPES = [
        ('icon', 'Icon'),
        ('logo', 'Logo'),
        ('poster', 'Poster'),
    ]

    SIZE_OPTIONS = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]

    STATUS_OPTIONS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(
        max_length=32, unique=True, null=False, editable=False)
    design_type = models.CharField(max_length=20, choices=DESIGN_TYPES)
    size = models.CharField(max_length=10, choices=SIZE_OPTIONS)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    status = models.CharField(
        max_length=20, choices=STATUS_OPTIONS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    field_upload = models.FileField(
        upload_to='orders/files', blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Order {self.order_number} by {self.user.username}"
            f" created at: {self.created_at}"
        )
