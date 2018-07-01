from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    class Meta:
        model = Order
    list_display = ['id','buyer', 'address', 'paid', 'created','updated','bukti_transfer']
    list_filter = ['paid', 'created', 'updated']
    list_editable = ['paid']
    inlines = [OrderItemInline,]

admin.site.register(Order, OrderAdmin)
# admin.site.unregister(Order, OrderAdmin)
