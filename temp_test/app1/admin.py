from django.contrib import admin                                                                                                                                  # type: ignore
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content','author', 'created_at', 'updated_at')
    list_filter = ('title', 'content')
    fieldsets = (
        ('Content', {'fields': ('title', 'content', 'is_published')}),
        ('Meta', {'fields': ('author', 'is_deleted')}),
    )

admin.site.register(Post, PostAdmin)
