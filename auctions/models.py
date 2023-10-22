from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    GENDER_CHOICES = [
        ('m', 'Masculin'),
        ('f', 'Féminin'),
    ]
    ichoices = [
       ('Phone & Tablet', 'Phone & Tablet'),
        ('Cooking & Culinary Arts', 'Cooking & Culinary Arts'),
        ('Health beauty', 'Health beauty'),
        ('Electronics', 'Electronics'),
        ('Supermarket', 'Supermarket'),
        ('Mode', 'Mode'),
        ('Informatique', 'Informatique'),
        ('Auto & Moto', 'Auto & Moto'),
        ('Home & Office', 'Home & Office'),
        ('Video Games & Consoles', 'Video Games & Consoles'),
        ('Sport stuff', 'Sport stuff'),
        # ... (other choices)
    ]

    telephone = models.CharField(max_length=20)
    city = models.CharField(max_length=100, blank=True, null=True)
    date_b = models.DateField(blank=True, null=True)
    interests = models.CharField(max_length=80, choices=ichoices, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    def __str__(self):
        return self.username

class Interest(models.Model):
    interest = models.CharField(primary_key=True, max_length=500, choices=[
        ('Phone & Tablet', 'Phone & Tablet'),
        ('Cooking & Culinary Arts', 'Cooking & Culinary Arts'),
        ('Health beauty', 'Health beauty'),
        ('Electronics', 'Electronics'),
        ('Supermarket', 'Supermarket'),
        ('Mode', 'Mode'),
        ('Informatique', 'Informatique'),
        ('Auto & Moto', 'Auto & Moto'),
        ('Home & Office', 'Home & Office'),
        ('Video Games & Consoles', 'Video Games & Consoles'),
        ('Sport stuff', 'Sport stuff'),
    ])

    def __str__(self):
        return self.interest

class Listing(models.Model):
    i_choices = [
        ('Phone & Tablet', 'Phone & Tablet'),
        ('Cooking & Culinary Arts', 'Cooking & Culinary Arts'),
        ('Health beauty', 'Health beauty'),
        ('Electronics', 'Electronics'),
        ('Supermarket', 'Supermarket'),
        ('Mode', 'Mode'),
        ('Informatique', 'Informatique'),
        ('Auto & Moto', 'Auto & Moto'),
        ('Home & Office', 'Home & Office'),
        ('Video Games & Consoles', 'Video Games & Consoles'),
        ('Sport stuff', 'Sport stuff'),
    ]
    
    price = models.CharField(max_length=20, null=True)
    user_f = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=150, primary_key=True, unique=True, blank=True )
    description = models.CharField(max_length=300)
    num_bids = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/')
    interests = models.CharField(max_length=80, choices=i_choices, blank=True, null=True)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='won_listings')

    def close_listing(self):
        self.active = False
        highest_bid = Bid.objects.filter(listing=self).order_by('-bid_amount').first()
        if highest_bid:
            self.winner = highest_bid.user
            self.save()

    def active_listing(self):
        self.active = True
        self.save()

    def delete(self, *args, **kwargs):
        self.num_bids -= 1
        self.save()
        super(Listing, self).delete(*args, **kwargs)

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    comment = models.CharField(max_length=50)
    comment_time = models.DateTimeField(default=timezone.now, editable=False)

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    title = models.CharField(max_length=150, null=True, blank=True)
    bid_time = models.DateTimeField(default=timezone.now, editable=False)

    def save(self, *args, **kwargs):
        is_new_bid = self.pk is None
        super(Bid, self).save(*args, **kwargs)
        if is_new_bid:
            self.listing.num_bids += 1
            self.listing.save()

    def delete(self, *args, **kwargs):
        self.listing.num_bids -= 1
        self.listing.save()
        super(Bid, self).delete(*args, **kwargs)



class Watchlist(models.Model):
    watchlist_id = models.AutoField(primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='watchlist', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)