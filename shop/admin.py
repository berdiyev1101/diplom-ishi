from django.contrib import admin
from shop.models import *

class ProductImageGather(admin.TabularInline):
    model = Gallery
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title","price","quantity"]
    list_display_links = ["title","price"]
    list_editable = ["quantity"]
    list_filter = ["price"]
    inlines = [ProductImageGather]

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Offer)
admin.site.register(Vendor)
admin.site.register(LatestBlog)
admin.site.register(Contact)
admin.site.register(Like)
admin.site.register(Basket)

