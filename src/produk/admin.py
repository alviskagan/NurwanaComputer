from django.contrib import admin
from .models import Produk, Kategori

# Register your models here.
class ProdukAdmin(admin.ModelAdmin):
    list_display = ('id_produk','nama_produk','kategori_produk','stok_produk','foto_produk','harga_produk','rating_produk')
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('id_kategori', 'nama_kategori')

admin.site.register(Produk, ProdukAdmin)
admin.site.register(Kategori, KategoriAdmin)