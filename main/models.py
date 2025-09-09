from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)         # nama item
    price = models.IntegerField()                   # harga item
    description = models.TextField()                # deskripsi item
    thumbnail = models.URLField()                   # gambar item (URL)
    category = models.CharField(max_length=50)      # kategori item
    is_featured = models.BooleanField(default=False)  # status unggulan

    def __str__(self):
        return f"{self.name} ({self.category})"
