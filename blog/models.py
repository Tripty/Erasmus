from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from ckeditor_uploader.fields import RichTextUploadingField  # enables editor + uploads

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Post(models.Model):
    STATUS = [
        ("draft", "Draft"),
        ("pending", "Pending Review"),        # for guest submissions
        ("published", "Published"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                               help_text="Set if created by a logged-in blogger/admin.")
    guest_name = models.CharField(max_length=100, blank=True)
    guest_email = models.EmailField(blank=True)

    content = RichTextUploadingField()   # CKEditor with upload button
    cover_image = models.ImageField(upload_to='blog/covers/', blank=True, null=True)

    categories = models.ManyToManyField(Category, blank=True, related_name='posts')

    status = models.CharField(max_length=20, choices=STATUS, default="draft")
    published_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  # logged-in commenter
    guest_name = models.CharField(max_length=100, blank=True)  # for guest commenters
    guest_email = models.EmailField(blank=True)
    body = models.TextField()

    is_approved = models.BooleanField(default=False)  # simple moderation

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        who = self.user or self.guest_name or "Anonymous"
        return f"Comment by {who} on {self.post}"

#
#class BlogPost(models.Model):
#   title = models.CharField(max_length=200)
#   content = models.TextField()
#   image = models.ImageField(upload_to="blog_images/", blank=True, null=True)
#   category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
#   author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#   created_at = models.DateTimeField(auto_now_add=True)
#   updated_at = models.DateTimeField(auto_now=True)

#   def __str__(self):
#       return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

