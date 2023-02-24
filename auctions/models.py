from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category_name}"

class Bid(models.Model):
    time = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return f"{self.user.username.capitalize()} placed a bid for {self.price}"



class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255, blank=True)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, null=True, related_name="bid_price" )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default="", blank=True, null=True, related_name="category")
    time = models.DateTimeField(auto_now_add=True, blank=True)
    closed = models.BooleanField(default=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sellers")
    image = models.CharField(max_length=1000, default="")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")
    bids = models.ManyToManyField(Bid, blank=True, related_name="bids")

    def __str__(self):
        return f"{self.title}: is {self.price} and is being sold by {self.seller}"



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default="", related_name="listing")
    comment = models.CharField(max_length=150, default="")
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} commented on {self.listing}"

