from django.shortcuts import render, get_object_or_404

from .models import Page
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.shortcuts import render
# ask chatgpt can i import from other app?
from blog.models import Post
from datetime import datetime


def homehome(request):
    latest_posts = Post.objects.order_by('-created_at')[:6]  # latest 6 posts

    # build full URLs for each post
    for post in latest_posts:
        post.full_cover_url = request.build_absolute_uri(settings.MEDIA_URL + post.cover_image)

    return render(request, "pages/home.html", {
        "latest_posts": latest_posts,
        "year": datetime.now().year,
    })
    
def home(request):
    latest_posts = Post.objects.order_by('-created_at')[:6]
    return render(request, "pages/home.html", {
        "latest_posts": latest_posts,
        "MEDIA_URL": settings.MEDIA_URL,
    })
    



def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render(request, "pages/page_detail.html", {"page": page})

def contact(request):
    form = ContactForm(request.POST or None)
    success = False

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        send_mail(
            f"Message from {data['name']}",
            data['message'],
            data['email'],
            [settings.DEFAULT_FROM_EMAIL],
        )
        success = True

    return render(request, "pages/contact.html", {"form": form, "success": success})
