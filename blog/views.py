from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm

from django.core.exceptions import PermissionDenied


from .models import Post, Category
from .forms import GuestPostForm, BloggerPostForm, CommentForm, BlogPostForm
from .models import ContactMessage


def post_list(request):
    qs = Post.objects.filter(status="published").order_by("-published_at", "-created_at")
    category_slug = request.GET.get("category")
    if category_slug:
        qs = qs.filter(categories__slug=category_slug)

    paginator = Paginator(qs, 5)  # 7) Pagination: 5 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    ctx = {"page_obj": page_obj, "categories": categories, "active_category": category_slug}
    return render(request, "blog/post_list.html", ctx)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status__in=["published", "draft", "pending"])

    # comments (show only approved)
    comments = post.comments.filter(is_approved=True).select_related("user")

    # handle new comment (guest or logged in)
    if request.method == "POST" and "add_comment" in request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.post = post
            if request.user.is_authenticated:
                c.user = request.user
                c.is_approved = True  # auto-approve logged-in users? your choice
            c.save()
            messages.success(request, "Comment submitted!" if not c.is_approved else "Comment posted.")
            return redirect("blog:post_detail", slug=post.slug)
    else:
        form = CommentForm()

    return render(request, "blog/post_detail.html",
                  {"post": post, "comments": comments, "comment_form": form})

def submit_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.is_approved = False  # Mark as pending review
            post.save()
            messages.success(request, "✅ Thank you! Your post was submitted. We will review it soon.")
            return redirect("blog:thank_you")   
    else:
        form = BlogPostForm()
    return render(request, "blog/submit_post.html", {"form": form})


def guest_post_create(request):
    """1) guest submission -> status pending, requires moderation."""
    if request.method == "POST":
        form = GuestPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.status = "pending"
            post.save()
            form.save_m2m()
            messages.success(request, "Thanks! Your post is submitted and awaiting review.")
            """  return redirect("post_list")
            messages.success(request, "✅ Thank you! Your post was submitted. We will review it soon.") """
            return redirect("blog:thank_you")
    else:
        form = GuestPostForm()
    return render(request, "blog/post_create_guest.html", {"form": form})


def user_is_blogger(user):
    return user.is_authenticated and (user.is_staff or user.groups.filter(name="Blogger").exists())

@login_required
def blogger_post_create(request): 
    if not user_is_blogger(request.user):
        raise PermissionDenied  
    """Authenticated bloggers/admins can publish directly."""
    if request.method == "POST":
        form = BloggerPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if post.status == "published" and not post.published_at:
                post.published_at = timezone.now()
            post.save()
            form.save_m2m()
            messages.success(request, "Post created.")
            return redirect("blog:post_detail", slug=post.slug)
    else:
        form = BloggerPostForm()
    return render(request, "blog/post_create_blogger.html", {"form": form})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Thank you for contacting us. We’ll reply soon!")
            return redirect("blog:contact")
    else:
        form = ContactForm()
    return render(request, "pages/contact.html", {"form": form})



def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "🎉 Your account has been created. Please log in.")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})
