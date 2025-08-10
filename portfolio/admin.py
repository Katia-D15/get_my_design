from django.contrib import admin
from .models import PortfolioItem


class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'design_type',
                    'visible',)

    ordering = ('-created_at', )


admin.site.register(PortfolioItem)
