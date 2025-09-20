from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)         # nama item
    price = models.IntegerField()                   # harga item
    description = models.TextField()                # deskripsi item
    thumbnail = models.URLField()                   # gambar item (URL)
    category = models.CharField(max_length=50)      # kategori item
    is_featured = models.BooleanField(default=False)  # status unggulan

    def __str__(self):
        return f"{self.name} ({self.category})"
