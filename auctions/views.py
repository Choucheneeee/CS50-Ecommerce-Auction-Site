from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import QueryDict
from django.contrib.auth import login


from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User,Listing,Interest,Comment
from django.shortcuts import render, get_object_or_404, redirect
from .models import User
from django.db.models import Count
from .models import Listing,Watchlist
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def index(request):
    # Define the criteria for active listings
    listings = Listing.objects.filter(active=True)
    all_listings = Listing.objects.all()  # Assuming you have an 'active' field

    # Annotate the number of bids for each active listing
    return render(request, 'auctions/index.html', {'active_listings': all_listings})


    


def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    return render(request, 'index.html', {'listing': listing})



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
    return redirect('login')



def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        telephone = request.POST["telephone"]
        city = request.POST["city"]
        interests = request.POST.getlist('interests')
        gender = request.POST.getlist('gender')      
        date_b = request.POST.get('date_b', None)

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create a new user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                telephone=telephone,
                city=city,
                interests=','.join(interests),
                gender=','.join(gender),
                date_b=date_b,
                password=password,
            )
            user.save()  # Call save() on the instance, not the model class
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    

def category(request):
    categories = Interest.objects.all()
    return render(request, 'auctions/category.html', {'categories': categories})


def category_view(request, category):
    # Retrieve listings for the specified category
    listings = Listing.objects.filter(interests=category)
    print(listings)
    return render(request, 'auctions/category_view.html',{'listings': listings})

def watchlist(request):
    return render(request, "auctions/watchlist.html")

from django.contrib.auth.decorators import login_required
from .models import User
@login_required

def creatlisting(request):
    missing_fields = []
    if request.method == "POST":
        user = request.user
        title = request.POST.get("title")
        description = request.POST.get("description")
        num_bids  = 0
        interests = request.POST.getlist("interest")
        price = request.POST.get("price")
        image = request.FILES.get('image')
        print(f"Title: {title}")
        print(f"Description: {description}")
        print(f" num_bids : { num_bids }")
        print(f"Price: {price}")
        print(f"Interests: {interests}")
        print(f"Image: {image}")
        print(f"user_f: {user}")
        # Attempt to create a new user
        if not title:
            missing_fields.append("Title")
        if not description:
            missing_fields.append("Description")
        if not price:
            missing_fields.append("Price")
        if not interests:
            missing_fields.append("Interests")
        if not image:
            missing_fields.append("Image")
        
        if missing_fields:
            return render(request, "auctions/creatlisting.html", {
                "message": f"Missing or invalid fields: {', '.join(missing_fields)}"
            })
        try:
            listing = Listing.objects.create(
                user_f=user,
                title=title,
                description=description,
                num_bids = num_bids ,
                price=price,
                interests=','.join(interests),
                image=image,
            )
            listing.save()
            return redirect('index')  # Call save() on the instance, not the model class
        except IntegrityError as e:
            print(f"IntegrityError: {e}")
            return render(request, "auctions/index.html", {
                "messages": "Listing valid."
            })
            
        return render(request, "auctions/index.html", {
                "message": "Listing successfully added "
            })    
    else:
        return render(request, "auctions/creatlisting.html")
    




from django.http import Http404

from django.shortcuts import render, get_object_or_404
from .models import Listing, Comment

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import Listing,Watchlist


from django.shortcuts import get_object_or_404, render
from .models import Listing

from django.contrib.auth.models import AnonymousUser

def product_view(request, title):
    listing = get_object_or_404(Listing, title=title)
    comments = listing.comments.all()

    # Check if the user is logged in
    if request.user.is_authenticated:
        # User is logged in
        var = Watchlist.objects.filter(user=request.user, listing=listing).exists()
    else:
        # User is not logged in (AnonymousUser)
        var = False  # You can set var to False or handle it differently

    return render(request, 'auctions/product_view.html', {'listing': listing, 'var': var, 'comments': comments})


from django.contrib import messages
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Listing, Bid
from django.urls import reverse
from django.shortcuts import redirect

from django.http import HttpResponseBadRequest

from django.http import HttpResponseBadRequest

def bid(request, title):
    listing = get_object_or_404(Listing, title=title)
    current_datetime = timezone.now()

    if request.method == 'POST':
        user = request.user
        bid_amount = request.POST.get('bid_amount')

        if bid_amount is not None:
            try:
                bid_amount = float(bid_amount)
            except ValueError:
                return HttpResponseBadRequest("Invalid bid amount format")

            # Check if the new bid is higher than the current highest bid
            highest_bid = Bid.objects.filter(listing=listing).order_by('-bid_amount').first()
            if highest_bid and bid_amount <= highest_bid.bid_amount:
                return HttpResponseBadRequest("Your bid must be higher than the current highest bid.")
            
            # Create a new bid
            bid = Bid(listing=listing, user=user, bid_amount=bid_amount, bid_time=current_datetime)
            listing.save()
            bid.save()

        # Use the PRG pattern - redirect to the bid page to prevent resubmission
        return redirect('bid', title=listing.title)

    # Handle GET requests here (e.g., initial page load)
    bids = Bid.objects.filter(listing=listing).order_by('-bid_amount')  # Get all bids for the listing
    return render(request, 'auctions/bid.html', {'listing': listing, 'bids': bids})



from django.shortcuts import render, redirect
from .models import Listing

from django.http import HttpResponseForbidden



@login_required
def close_listing_view(request, title):
    listing = get_object_or_404(Listing, title=title)

    # Check if the listing meets your closing condition (e.g., when a certain time has passed)
    # You can add your own condition here
    if listing.close_listing:
        listing.close_listing()
    

        # The listing is closed, and the winner is set
        return HttpResponse("Listing closed successfully. The winner is: " + listing.winner.username)
    else:
        return HttpResponse("The listing is not eligible to be closed yet.")



from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from django.shortcuts import redirect, get_object_or_404
from .models import Listing, Comment
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import get_object_or_404, redirect
from .models import Listing, Comment
from django.contrib.auth.models import User  # Import User model

from auctions.models import User  # Import your custom User model

def add_comment(request, title):
    if request.method == 'POST':
        # Explicitly retrieve the user by username # Use username
        comment_text = request.POST.get('comment_text')
        if comment_text:
            # Find the listing
            listing = get_object_or_404(Listing, title=title)
            # Create a new comment and link it to the listing and the current user
            comment = Comment(listing=listing, comment=comment_text)
            comment.save()

    return redirect('product_view', title=title)



from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def add_watchlist(request, title):
    if request.method == 'POST':
        
        listing = get_object_or_404(Listing, title=title)
        watchlist = Watchlist(listing=listing,user = request.user)
        watchlist.save()

    return redirect('product_view', title=title)

@login_required
def delete_watchlist(request, title):
    if request.method == 'POST':
        listing = get_object_or_404(Listing, title=title)
        user = request.user

        try:
            # Try to get the watchlist entry for the listing and user
            watchlist = Watchlist.objects.get(listing=listing, user=user)
            watchlist.delete()
        except Watchlist.DoesNotExist:
            # Handle the case where the listing is not in the user's watchlist
            pass

    return redirect('product_view', title=title)

from django.shortcuts import render
from .models import Watchlist, Listing

def watchlist_view(request):
    if request.user.is_authenticated:  # Check if the user is authenticated (logged in)
        user = request.user
        watchlists = Watchlist.objects.filter(user=user)
        listings = [watchlist.listing for watchlist in watchlists]
    else:
        user = None  # You can set a default user or handle this case differently
        watchlists = []
        listings = []

    return render(request, 'auctions/watchlist.html', {'listings': listings, 'watchlists': watchlists, 'user': user})