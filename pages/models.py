from django.db import models

class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # created once
    updated_at = models.DateTimeField(auto_now=True)      # updated each save

    def __str__(self):
        return self.title   