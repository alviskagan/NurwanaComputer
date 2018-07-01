from django.contrib import admin
from .models import Produk, Kategori, Rating
from django.contrib.auth.models import User


# Register your models here.
class ProdukAdmin(admin.ModelAdmin):
    list_display = ('id_produk','nama_produk','kategori_produk','stok_produk','foto_produk','harga_produk')
    list_editable = ['stok_produk','harga_produk','foto_produk']
    list_per_page = 10
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('id_kategori', 'nama_kategori')    



class RatingAdmin(admin.ModelAdmin):

    list_display = ('id_rating', 'id_pelanggan', 'id_produk', 'is_rating')
    
        
admin.site.register(Produk, ProdukAdmin)
admin.site.register(Kategori, KategoriAdmin)
admin.site.register(Rating, RatingAdmin)