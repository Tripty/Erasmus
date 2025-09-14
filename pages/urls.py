from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path('', views.home, name='pages_home'),  # for /pages/
    path('contact/', views.contact, name="contact"),
    path('<slug:slug>/', views.page_detail, name="page_detail"),

]
