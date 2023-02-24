from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.new_listing, name="create"),
    path("display_category", views.display_category, name="display_category"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watchlist", views.display_watchlist, name="watchlist"),
    path('watchlist/<int:id>/', views.toggle_watchlist, name='toggle_watchlist'),
    path("add_comment/<int:id>", views.add_comment, name="add_comment"),
    path("place_bid/<int:id>", views.place_bid, name="place_bid"),
    path("close_auction/<int:id>", views.close_auction, name="close_auction")    
]
