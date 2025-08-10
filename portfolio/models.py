from django.db import models
from core.choices import DesignTypeChoices


class PortfolioItem(models.Model):
    """
    Represents a single item in the portfolio
    """
    title = models.CharField(max_length=100)
    design_type = models.CharField(
        max_length=20,
        choices=DesignTypeChoices.choices,
        null=False, blank=False
        )
    image = models.ImageField(
        upload_to='portfolio/images', blank=True, null=True)
    description = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_design_type_display()})"
