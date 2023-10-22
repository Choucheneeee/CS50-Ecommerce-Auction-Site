from django.contrib import admin
from .models import User,Interest,Listing,Comment,Bid,Watchlist

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "telephone", "city","interests","gender")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("user_f", "title", "description","num_bids","image","interests","price")

class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_id', 'listing','comment','comment_time')

# Register your model with the custom admin class

class BidAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'bid_amount', 'bid_time')

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_f', 'price', 'num_bids', 'interests')

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('watchlist_id','user', 'listing')



admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid,BidAdmin)
admin.site.register(Interest)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
