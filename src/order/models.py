from django.db import models
from produk.models import Produk
from django.contrib.auth.models import User
from datetime import datetime, timedelta
# Create your models here.


class Order(models.Model):
    # pelanggan    = models.ForeignKey(
    #     User,
    #     on_delete   = models.CASCADE,
    #     related_name= 'order_pelanggan'
    # )
    buyer = models.ForeignKey(User, on_delete= models.CASCADE)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    address = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    bukti_transfer = models.ImageField(upload_to='transfer/%Y/%m/%d', blank=True)

    # def content_file_name(instance, filename):
    #     ext 		= filename.split('.')[-1]
    #     filename 	= "%s_%s.%s" % (instance.updated, instance.email, ext)
    #     return os.path.join('transfer', filename)   
        
    # bukti_transfer 	= models.FileField(upload_to= content_file_name ,null = True, blank = True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Produk, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
