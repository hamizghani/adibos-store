from django.db import models
from django.contrib.auth.models import User
import uuid

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

class Student(models.Model):
    student_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    batch = models.IntegerField()
    biodata = models.TextField()

class Book(models.Model):
    book_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    num_page = models.IntegerField()
    description = models.TextField()

class Author(models.Model):
    author_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # allow linking to an optional User; require on_delete
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    biodata = models.TextField()
    books = models.ManyToManyField(Book, blank=True)



    