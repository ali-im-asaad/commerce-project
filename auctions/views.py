from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    active_listings = Listing.objects.filter(closed=False)
    all_categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": active_listings,
        "categories": all_categories
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def listing(request, id):
    listing_data = Listing.objects.get(pk=id)
    all_comments = Comment.objects.filter(listing=listing_data)
    isSeller = request.user.username == listing_data.seller.username
    result = render(request, "auctions/listing.html", {
         "listing": listing_data,
         "all_comments": all_comments,
         "isSeller": isSeller
    })
    return result


def new_listing(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/new_listing.html", {"categories": categories})
    
    title = request.POST["title"]
    description = request.POST["description"]        
    image_url = request.POST["imageurl"]        
    price = float(request.POST["price"])   
    category = Category.objects.get(category_name=request.POST["category"]) 
    current_user = request.user     
    bid = Bid.objects.create(price=price, user=current_user)
    
    Listing.objects.create(
        title=title,
        description=description,
        image=image_url,
        price=bid,
        category=category,
        seller=current_user
    )

    return HttpResponseRedirect(reverse("index"))


def display_category(request):
    if request.method == "POST":
        selected_category = request.POST['category']
        category = Category.objects.get(category_name=selected_category)
        active_listings = Listing.objects.filter(closed=False, category=category)
        all_categories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": active_listings,
            "categories": all_categories,
            "selected_category": category,
        })        

def display_watchlist(request):
    user = User.objects.get(username=request.user)
    return render(request, "auctions/watchlist.html", {
    "watchlist": user.watchlist.all()
})


def toggle_watchlist(request, id):
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user

    if current_user in listing_data.watchlist.all():
        listing_data.watchlist.remove(current_user)
    else:
        listing_data.watchlist.add(current_user)

    return HttpResponseRedirect(reverse("listing", args=(id, )), {
        "listing": listing_data,
    })


def add_comment(request, id):
    
    listing_data = Listing.objects.get(pk=id)
    comment = Comment.objects.create(
        user=request.user,
        listing=listing_data,
        comment=request.POST["new_comment"]
    )

    return HttpResponseRedirect(reverse("listing", args=(id, )))



def place_bid(request, id):
    listing_data = Listing.objects.get(pk=id)
    user = request.user

    if user != listing_data.seller:
        new_bid = float(request.POST["new_bid"])

        if new_bid > listing_data.price.price:
            update_bid = Bid.objects.create(user=user, price=new_bid)
            listing_data.price = update_bid
            listing_data.save()
            message = "You have posted a new bid!"
            update = True
        else:
            message = "Error: very low bid! Step up your game."
            update = False

        all_comments = Comment.objects.filter(listing=listing_data)    
        return render(request, "auctions/listing.html", {
            "listing": listing_data,
            "message": message,
            "update": update,
            "new_bid": new_bid,
            "all_comments": all_comments
        })
    return render(request, "auctions/listing.html", {
        "listing": listing_data,
        "message": "You can't place a bid, you are the seller!"
    })
       


def close_auction(request, id):
    listing_data = Listing.objects.get(pk=id)
    listing_data.closed = True  
    listing_data.save()
    return render(request, "auctions/listing.html", {
    "listing": listing_data,
    "update": True,
    "message": "Congrats! The auction is closed!",
})          



