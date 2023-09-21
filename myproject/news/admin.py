from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import *

admin.site.register(News)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(NewsTopic)
admin.site.register(NewsRecommend)