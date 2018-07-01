from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.deconstruct import deconstructible
from django.contrib.auth.models import User
from django.urls import reverse


# from order.models import OrderItem

# Create your models here.
class Kategori (models.Model):
    id_kategori 	= models.AutoField(primary_key= True)
    # slug = models.SlugField(max_length=150, unique=True ,db_index=True)
    nama_kategori 	= models.CharField(max_length= 250)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('nama_kategori', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.nama_kategori

    # def get_absolute_url(self):
    #     return reverse('produk:produk_list_by_category', args=[self.slug])

    def __str__(self):
        return self.nama_kategori

class Produk(models.Model):
    id_produk 		= models.AutoField(primary_key = True)
    nama_produk 	= models.CharField(max_length = 250)
    kategori_produk = models.ForeignKey(
        Kategori,
        null 		= False,
        on_delete 	= models.CASCADE,
        related_name= 'kategori',
        unique 		= False
    )
    stok_produk 	= models.IntegerField()    
    harga_produk 	= models.IntegerField()
    
    rating_produk 	= models.IntegerField(default = 0) 
    deskripsi       = models.TextField(max_length=255, blank=True)
    #Untuk mengubah nama file yang diupload lalu disimpan ke dalam folder foto 
    def content_file_name(instance, filename):
        ext 		= filename.split('.')[-1]
        filename 	= "%s_%s_%s.%s" % (instance.id_produk, instance.kategori_produk, instance.nama_produk, ext)
        return os.path.join('foto', filename)   
        
    foto_produk 	= models.FileField(upload_to= content_file_name ,null = True, blank = True)

    class Meta:
        ordering = ('nama_produk', )
        index_together = (('id_produk', 'kategori_produk'),)

    def __str__(self):
        return self.nama_produk

    def get_absolute_url(self):
        return reverse('produk:produk_detail', args=[self.id_produk, self.kategori_produk])
    
    # def update_stok(self):
    #     order_items.quantity



class Rating(models.Model):
    id_rating       = models.AutoField(primary_key= True)
    id_pelanggan    = models.ForeignKey(
        User,
        on_delete   = models.CASCADE,
        related_name= 'rating_pelanggan'
    )
    id_produk       = models.ForeignKey(
        Produk,
        on_delete   = models.CASCADE,
        related_name= 'rating_id_produk'
    )
    rating_choices  = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ) 
    is_rating       = models.IntegerField(choices= rating_choices, default = 0)