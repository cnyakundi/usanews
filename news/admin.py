from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Post


@admin.register(Post)
class PosteAdmin(admin.ModelAdmin):
    list_display = ("media_house_name", "title", "pub_date")
