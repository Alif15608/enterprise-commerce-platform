from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ["line_total"]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "session_token", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["user__email", "session_token"]
    inlines = [CartItemInline]