from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    link = models.URLField()
    media_house_name = models.CharField(max_length=200)
    image = models.URLField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    guid = models.CharField(max_length=50)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='published')

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title
