from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_comment/<str:title>/', views.add_comment, name='add_comment'),
    path('delete_comment/<str:title>/', views.delete_watchlist, name='delete_watchlist'), 
    path('add_watchlist/<str:title>/', views.add_watchlist, name='add_watchlist'),
    path('listing/toggle_activation/<str:title>/', views.close_listing_view, name='toggle_listing_activation'),
    path('bid/<str:title>/', views.bid, name='bid'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('category/', views.category, name='category'),        # Add a slash at the end
    path('category/<str:category>/', views.category_view, name='category_view'),
    path('product/<str:title>/', views.product_view, name='product_view'),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("creatlisting", views.creatlisting, name="creatlisting")
]
