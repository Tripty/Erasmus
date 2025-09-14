from django.contrib import admin
from .models import Post , Category, Comment


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ("name",)

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ("user", "guest_name", "guest_email", "body", "is_approved", "created_at")
    readonly_fields = ("created_at",)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "published_at", "updated_at")
    list_filter = ("status", "categories", "author")
    search_fields = ("title", "content")
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ("categories",)
    inlines = [CommentInline]
    date_hierarchy = "published_at"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "guest_name", "is_approved", "created_at")
    list_filter = ("is_approved", "created_at")
    search_fields = ("body", "guest_name", "guest_email")


