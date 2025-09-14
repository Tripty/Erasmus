from django import forms
from .models import Post, Comment, Category
from ckeditor.widgets import CKEditorWidget
from .models import ContactMessage


class GuestPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget()) 
    class Meta:
        model = Post
        fields = ["title", "guest_name", "guest_email", "content", "cover_image", "categories"]
        widgets = {
            "categories": forms.CheckboxSelectMultiple
        }

class BloggerPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "cover_image", "categories", "status", "published_at"]
        widgets = {
            "categories": forms.CheckboxSelectMultiple
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body", "guest_name", "guest_email"]


class BlogPostForm(forms.ModelForm):
    # Replace normal textarea with CKEditor
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        #model = BlogPost
        model = Post
        
        fields = ["title", "guest_name", "guest_email", "content", "cover_image" , "categories"]


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
