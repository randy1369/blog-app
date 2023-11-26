from django.contrib import admin
from .models import Categories, Tag, BlogPost, Subcategories
# Register your models here.

admin.site.register(BlogPost)
admin.site.register(Categories)
admin.site.register(Subcategories)
admin.site.register(Tag)