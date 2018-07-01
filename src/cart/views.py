# from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from produk.models import Produk, Kategori
from .cart import Cart
from .forms import CartAddProductForm
from django.http import HttpResponse
from django.contrib import messages

# from allauth.account.decorators import verified_email_required

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Produk, id_produk=product_id)
    stok = Produk.objects.get(id_produk__exact = product_id).stok_produk
    all_produks = Produk.objects.filter(id_produk__exact = product_id ).select_related('kategori_produk')
    all_kategori = Kategori.objects.all()
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        if cd['quantity'] <= stok and cd['quantity'] > 0:
            cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
            return redirect('cart:cart_detail')
        else:
            cart_product_form = CartAddProductForm()
            produk = {
                "data_produk": all_produks,
                'cart_product_form': cart_product_form,
                "kategori_produk": all_kategori
            }
            messages.warning(request, 'Jumlah angka yang anda masukkan melebihi stok.')
            return render(request, 'produk/detail_produk.html', produk) 
    else:
        cart_product_form = CartAddProductForm()
        produk = {
            "data_produk": all_produks,
            'cart_product_form': cart_product_form,
            "kategori_produk": all_kategori
        }
        messages.warning(request, 'Jumlah angka yang anda masukkan salah.') 
        return render(request, 'produk/detail_produk.html', produk)



def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Produk, id_produk=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})