from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.deconstruct import deconstructible
from django.contrib.auth.models import User
# Create your models here.
class Kategori (models.Model):
    id_kategori 	= models.AutoField(primary_key= True)
    nama_kategori 	= models.CharField(max_length= 250)
    synset          = models.CharField(max_length=255, null =True)
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
    
    rating_produk 	= models.IntegerField() 
    deskripsi       = models.TextField(max_length=255, blank=True)
    #Untuk mengubah nama file yang diupload lalu disimpan ke dalam folder foto 
    def content_file_name(instance, filename):
        ext 		= filename.split('.')[-1]
        filename 	= "%s_%s_%s.%s" % (instance.id_produk, instance.kategori_produk, instance.nama_produk, ext)
        return os.path.join('foto', filename)   
        
    foto_produk 	= models.FileField(upload_to= content_file_name ,null = True, blank = True)

    def __str__(self):
        return self.nama_produk

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