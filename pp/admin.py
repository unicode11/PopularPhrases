from django.contrib import admin

from .models import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("text", "title", "weight", "likes", "dislikes")
    search_fields = ("text", "title")
    list_filter = ("title",)
