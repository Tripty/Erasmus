from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

app_name = "blog"


urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("submit/guest", views.guest_post_create, name="guest_post_create"),         # guest submit
    path("submit/blogger", views.submit_post, name="submit_post"),
    path("new/", views.blogger_post_create, name="blogger_post_create"),        # blogger create
    path("thank-you/", TemplateView.as_view(template_name="blog/thank_you.html"), name="thank_you"),
    path("register/", views.register, name="register"),
    path("<slug:slug>/", views.post_detail, name="post_detail"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", views.post_list, name="blog:post_list"),
    





   # path("", views.blog_home, name="blog_home"),


  
    #path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),


]
