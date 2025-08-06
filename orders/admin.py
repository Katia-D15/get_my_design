from django.contrib import admin
from .models import Order, Comment


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


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'public_name',
                    'approved',
                    'created_at',)

    list_filter = ('approved',
                   'created_at',
                   'order__design_type',
                   )

    ordering = ('-created_at', )


admin.site.register(Comment, CommentAdmin)
