from django.shortcuts import render
from .models import OrderItem, Order
from .forms import OrderCreateForm, UploadBuktiTransfer, RatingForm
from cart.cart import Cart
from profile.models import Customer
from produk.models import Produk, Rating
from django.contrib.auth.models import User

import os
from allauth.account.decorators import verified_email_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
# from django.core.files.storage import FileSystemStorage
from django.db import connection
import numpy as np
import pandas as pd

@verified_email_required(login_url='/accounts/login/')
def order_create(request, no_order = 0):
    cart = Cart(request)
    user_id = request.user.id
    # print(usernm, "username")
    user_fn		= User.objects.get(id__exact = user_id).first_name
    user_ln		= User.objects.get(id__exact = user_id).last_name
    user_em		= User.objects.get(id__exact = user_id).email
   
    # if request.method == "POST":
    #     form_upload = UploadBuktiTransfer(request.POST)
    #     if form_upload.is_valid() and no_order != 0:
    #         cd = form_upload.cleaned_data
    #         print(cd['bukti_transfer'])
    #         Order.objects.filter(order__exact = no_order).create(bukti_transfer = cd['bukti_transfer'])
    #         messages.warning(request, 'Pembayaran Berhasil!')
    #         return render(request, 'message.html') 
    #     # all_produks = Produk.objects.filter(id_produk__exact = id ).select_related('kategori_produk')
    #     # validasi apabila data profile belum lengkap, maka akan muncul notifikasi untuk segera melengkapi profile
    #     # order = None
    #     # if user_fn != None and user_ln != None and user_add != None and user_em != None:
    # else:    
    if cart.session.get(settings.CART_SESSION_ID) != {}:
        form_upload = UploadBuktiTransfer()
        order = Order.objects.create(
            first_name = user_fn,
            last_name = user_ln,
            email = user_em,
            # address = user_add
        )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
        )
        order_item = OrderItem.objects.filter(order__exact = order)
        order_data = Order.objects.filter(id__exact = order.id)
        produk = {
            "data_produk": order_item,
            "order_id"   : order,
            "data_order" : order_data,
            "form_upload": form_upload
        }
        
        cart.clear()

        messages.warning(request, 'Cart anda sudah disimpan, silahkan cek riwayat order anda')
        return render(request, 'order/invoice.html', produk)
    else:
        messages.warning(request, 'Silahkan Lengkapi Data Anda Terlebih Dahulu')
        # return render(request, 'message.html')
        return redirect('order:order_create')

@verified_email_required(login_url='/accounts/login/')
def upload_bukti(request, no_order):
    cart = Cart(request)
    order = Order.objects.get(id__exact = no_order)
    if request.method == 'POST':
        form = UploadBuktiTransfer(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['image']
            cursor = connection.cursor()
            # Update stok
            produk = pd.read_sql_query("select product_id, quantity from order_orderitem where order_orderitem.order_id = "+str(no_order)+"", connection)
            for line in produk.itertuples():
                stok = Produk.objects.get(id_produk__exact = line[1]).stok_produk
                new_stok = stok - line[2]
                cursor.execute("update produk_produk set stok_produk = "+str(new_stok)+" where produk_produk.id_produk = "+str(line[1])+ "")
                print(line[1], line[2], stok)
            
            # Validasi Apakah product_id pada OrderItem sudah pernah dirating atau belum? 
            # rating = pd.read_sql_query("select order_orderitem.product_id from order_orderitem, produk_rating where order_orderitem.order_id = "+str(no_order)+" and produk_rating.id_pelanggan_id = "+str(request.user.id)+" and produk_rating.id_produk_id = order_orderitem.product_id and produk_rating.is_rating = 0", connection)
            # produk_id = pd.read_sql_query("select product_id from order_orderitem where order_orderitem.order_id = "+str(no_order)+"", connection)
        
            produk_id = pd.read_sql_query("select distinct order_orderitem.product_id from order_orderitem ,order_order where order_orderitem.order_id = order_order.id  and order_order.buyer_id = "+str(request.user.id)+" and order_orderitem.product_id not in (select produk_rating.id_produk_id from produk_rating where produk_rating.id_pelanggan_id = "+str(request.user.id)+")", connection)
            daftar_rating = []
            for line in produk_id.itertuples():
                id_produk_rating = line[1]
                daftar_rating += Produk.objects.filter(id_produk__exact = id_produk_rating)
            
            # produk_rating = OrderItem.objects.filter(order__exact = no_order)
            print(daftar_rating)
            order.bukti_transfer = image
            order.save()
            cart.clear()
            form = RatingForm()
            data = {
                'produk_rating': daftar_rating,
                'form'         : form
            }
            messages.success(request, 'Upload Berhasil!')
            messages.warning(request, 'Silahkan berikan rating pada produk yang sudah pernah anda beli.')
            return render(request, 'produk/rating.html', data)
    else:
        form = UploadBuktiTransfer()
        messages.warning(request, 'Cart anda sudah disimpan, silahkan cek riwayat order anda')
    
    order_item = OrderItem.objects.filter(order__exact = order)
    order_data = Order.objects.filter(id__exact = order.id)
    produk = {
        "data_produk": order_item,
        "order_id"   : order,
        "data_order" : order_data,
        "form_upload": form
    }
    
    messages.warning(request, 'Cart anda sudah disimpan, silahkan cek riwayat order anda')
    return render(request, 'order/invoice.html', produk)
    # return render(request, 'message.html')

@verified_email_required(login_url='/accounts/login/')
def order_form(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid() and cart.session.get(settings.CART_SESSION_ID) != {}:
            # cd = form.cleaned_data()
            user_id = request.user.id
            form_upload = UploadBuktiTransfer()

            # user_fn		= User.objects.get(id__exact = user_id).first_name
            # user_ln		= User.objects.get(id__exact = user_id).last_name
            # user_em		= User.objects.get(id__exact = user_id).email
            # order = Order.objects.create(
            #     first_name = cd['first_name'],
            #     last_name = cd['last_name'],
            #     email = cd['email'],
            #     address = cd['address'],
            #     postal_code = cd['postal_code']
            # )
            order = form.save()
            order.buyer = request.user
            print(order.save())
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
            )
            order_item = OrderItem.objects.filter(order__exact = order)
            order_data = Order.objects.filter(id__exact = order.id)
            produk = {
                "data_produk": order_item,
                "order_id"   : order,
                "data_order" : order_data,
                "form_upload": form_upload
            }
            
            messages.warning(request, 'Cart anda sudah disimpan, silahkan cek riwayat order anda')
            return render(request, 'order/invoice.html', produk)
            
        else:
            form = OrderCreateForm()
            return render(request, 'order/create.html', {'form': form})
    else:
        form = OrderCreateForm()
        return render(request, 'order/create.html', {'form': form})

def rating(request, id_produk):
    if request.method == "POST":
        form = RatingForm(request.POST)
        # print(form)
        if form.is_valid():
            print(id_produk)
            # cd = form.cleaned_data()
            add_rating = Rating.objects.create(
                id_pelanggan = request.user,
                id_produk_id = id_produk,
                is_rating = request.POST.get('rating')
            )
            add_rating.save()

            produk_id = pd.read_sql_query("select distinct order_orderitem.product_id from order_orderitem ,order_order where order_orderitem.order_id = order_order.id  and order_order.buyer_id = "+str(request.user.id)+" and order_orderitem.product_id not in (select produk_rating.id_produk_id from produk_rating where produk_rating.id_pelanggan_id = "+str(request.user.id)+")", connection)
            daftar_rating = []
            for line in produk_id.itertuples():
                id_produk_rating = line[1]
                daftar_rating += Produk.objects.filter(id_produk__exact = id_produk_rating)
            
            hasil_rating = pd.read_sql_query("select sum(is_rating)/count(id_rating) as Rating from produk_rating where produk_rating.id_produk_id = "+str(id_produk)+"", connection)
            for line in hasil_rating.itertuples():
                produk_rating = Produk.objects.get(id_produk__exact = id_produk)
                produk_rating.rating_produk = line[1]
                produk_rating.save()
                # cursor.execute("update produk_produk set stok_produk = "+str(new_stok)+" where produk_produk.id_produk = "+str(line[1])+ "")
                
            # produk = Produk.objects.get(id_produk__exact = id_produk)
            
            data = {
                'produk_rating': daftar_rating,
                'form'         : form
            }
            if daftar_rating != []:
                messages.warning(request, 'Rating Berhasil')
                return render(request, 'produk/rating.html', data)
            else:
                messages.warning(request, 'Produk yang anda beli sudah pernah anda beri rating')
                return render(request, 'message.html')
        return render(request, 'message.html')