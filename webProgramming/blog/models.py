from django.db import models
from django.utils import timezone
import os

GENDERR_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)
PROGRAM_CHOICES = (
    ('Computer Engineering', 'Computer Engineering'),
    ('Electrical Engineering', 'Electrical Engineering'),
    ('Psychology', 'Psychology'),
    ('Architecture', 'Architecture'),
    ('Industrial Engineering', 'Industrial Engineering'),
    ('Civil Engineering', 'Civil Engineering'),
)


class User(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    username = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=40)
    gender = models.CharField(max_length=29, choices=GENDERR_CHOICES, default='male')
    program = models.CharField(max_length=29, choices=PROGRAM_CHOICES, default='comp')
    isAdmin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Admin(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=20)


TOPIC_CHOICES = (
    ('announcements', 'Announcements'),
    ('complaints', 'Complaints'),
)


class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(primary_key=True, max_length=40)
    text = models.TextField()
    type = models.CharField(max_length=29, choices=TOPIC_CHOICES, default='type')
    publishDate = models.DateTimeField()

    def publish(self):
        self.publishDate = timezone.now()
        self.save()

    def __str__(self):
        return self.topic


GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
)
SIZE_CHOICES = (
    ('2xl', '2XL'),
    ('xl', 'XL'),
    ('l', 'L'),
    ('m', 'M'),
    ('s', 'S'),
    ('xs', 'XS'),

)
TYPEE_CHOICES = (
    ('shirts', 'Shirts'),
    ('trousers', 'Trousers'),
    ('shoes', 'Shoes'),
    ('Hoodies', 'Hoodies'),

)


class Product(models.Model):
    name = models.CharField(max_length=40)
    size = models.CharField(max_length=50, choices=SIZE_CHOICES, default='2xl')
    Id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, choices=TYPEE_CHOICES, default='shirts')
    gender = models.CharField(max_length=29, choices=GENDER_CHOICES, default='male')
    stock = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    image = models.ImageField(null=True)

    def __Int__(self):
        return self.Id


class Purchase(models.Model):
    purchaseId = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    productId = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    amount = models.IntegerField(null=True)
    totalPrice = models.IntegerField(null=True)


class Event(models.Model):
    name = models.CharField(primary_key=True, max_length=40)
    date = models.DateField(null=True)
    place = models.CharField(max_length=40)
    organizator = models.CharField(max_length=80)
    content = models.TextField(null=True)
    image1 = models.ImageField(null=True)


class shuttleHours(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    quota = models.IntegerField(null=True)
    hour = models.CharField(max_length=10, null=True)


class News(models.Model):
    topic = models.CharField(primary_key=True, max_length=150)
    content = models.TextField(null=True)
    image = models.ImageField(null=True)
    publishDate = models.DateTimeField(null=True)


class Reply(models.Model):
    replyId = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()


class Notes(models.Model):
    id = models.AutoField(primary_key=True)
    lesson = models.CharField(max_length=40)
    topic = models.CharField(max_length=40)
    note = models.FileField(max_length=1350)
