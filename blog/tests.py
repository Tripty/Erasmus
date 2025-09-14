from django.test import TestCase
from django.contrib.auth.models import User
from .models import BlogPost, Category

class BlogPostTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="tester", password="pass1234")
        # Create a category
        self.category = Category.objects.create(name="Tech")
        # Create a blog post
        self.post = BlogPost.objects.create(
            title="My First Post",
            content="Hello World",
            author=self.user,
            category=self.category,
        )

    def test_post_creation(self):
        """Check if post is created correctly"""
        self.assertEqual(self.post.title, "My First Post")
        self.assertEqual(self.post.author.username, "tester")
        self.assertEqual(self.post.category.name, "Tech")

    def test_post_str(self):
        """Check __str__ returns title"""
        self.assertEqual(str(self.post), "My First Post")
