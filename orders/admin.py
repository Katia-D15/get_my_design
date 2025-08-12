from django.contrib import admin, messages
from .models import Order, Comment


@admin.action(
    description="Mark selected orders as completed "
    "(only if confirmed and final file present)")
def mark_as_completed(modeladmin, request, queryset):
    """
    Mark selected orders as completed if they are confirmed
    and have a final file.

    Shows success/warning messages with counts of updated and skipped orders.
    """
    total = queryset.count()
    to_complete = (
        queryset
        .filter(status='confirmed')
        .exclude(final_file__isnull=True)
        .exclude(final_file='')
    )
    updated = to_complete.update(status='completed')
    skipped = total - updated

    if updated:
        modeladmin.message_user(
            request, f"{updated} order(s) marked as completed.",
            level=messages.SUCCESS
        )
    if skipped:
        modeladmin.message_user(
            request, f"{queryset.count() - updated} skipped "
            "(not confirmed or no final file.)",
            level=messages.WARNING)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number',
                    'user',
                    'design_type',
                    'size',
                    'price',
                    'status',
                    'created_at',)
    list_filter = ('status',
                   'design_type',)

    ordering = ('-created_at', )

    actions = [mark_as_completed]


admin.site.register(Order, OrderAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'public_name',
                    'approved',
                    'created_at',
                    'order_status',
                    )

    list_filter = ('approved',
                   'created_at',
                   'order__design_type',
                   )

    ordering = ('-created_at', )

    readonly_fields = ('order_status',)

    def order_status(self, obj):
        """
        Return the related Order status for display in CommentAdmin.
        """
        return obj.order.status if obj.order else None
    order_status.short_description = 'Status Order'
    order_status.admin_order_field = 'order__status'


admin.site.register(Comment, CommentAdmin)
