from decimal import Decimal
from django.conf import settings
from produk.models import Produk
from django.http import HttpResponse

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id_produk)
        stok = Produk.objects.get(id_produk__exact = product_id).stok_produk
        print(stok)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.harga_produk)}
            # self.save()x   
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
            # self.save()
        else:
            self.cart[product_id]['quantity'] += quantity
            # self.save()
        
            # self.cart[product_id]['quantity'] = stok
        if self.cart[product_id]['quantity'] <= stok:
            self.save()     
          
        # elif self.cart[product_id]['quantity'] > stok:
            # return  HttpResponse("Kuantitas yang dipilih melebihi stok yang ada")
            # return  HttpResponse("Text only, please.", content_type="text/plain")
            # response = HttpResponse("Kuantitas yang dipilih melebihi stok yang ada")
            # raise forms.ValidationError("Kuantitas yang dipilih melebihi stok yang ada")

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id_produk)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Produk.objects.filter(id_produk__in=product_ids)
        for product in products:
            self.cart[str(product.id_produk)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
