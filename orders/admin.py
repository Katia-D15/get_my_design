from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number',
                    'user',
                    'design_type',
                    'size',
                    'price',
                    'status',
                    'created_at',)

    ordering = ('-created_at', )


admin.site.register(Order, OrderAdmin)
