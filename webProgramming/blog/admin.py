from django.contrib import admin
from blog.models import User
from .models import Post,Reply
from .models import Product, shuttleHours, Notes
from .models import News
from .models import Event
from .models import Purchase
# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Product)
admin.site.register(News)
admin.site.register(Event)
admin.site.register(Purchase)
admin.site.register(Reply)
admin.site.register(shuttleHours)
admin.site.register(Notes)