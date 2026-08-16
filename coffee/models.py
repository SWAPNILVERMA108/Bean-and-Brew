from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 


# Create your models here.
class CoffeeVariety(models.Model):
    COFFEE_TYPE_CHOICE=[
        ('EP','ESPRESSO'),
        ('AM','AMERICANO'),
        ('CP','CAPPUCCINO'),
        ('LT','LATTE'),
        ('MC','MOCHA')
    ]
    name = models.CharField(max_length=100)
    image=models.ImageField(upload_to="coffee/")
    date_added = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=2,choices=COFFEE_TYPE_CHOICE)
    description = models.TextField(default='')

    def __str__(self):
        return self.name

# one to many 
class coffeeReview(models.Model):
    coffee = models.ForeignKey(CoffeeVariety, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f'{self.user.username} review for {self.coffee.name}'


## Many to Many 

class Store(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    coffee_varieties = models.ManyToManyField(CoffeeVariety,related_name='stores')
    staff_members = models.ManyToManyField(User, related_name='managed_stores', blank=True)

    def __str__(self):
        return self.name


class CoffeeOrder(models.Model):
    class Status(models.TextChoices):
        NEW = 'NEW', 'New request'
        ACCEPTED = 'ACCEPTED', 'Accepted by store'
        READY = 'READY', 'Ready for collection'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coffee_orders')
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='orders')
    coffee_variety = models.ForeignKey(CoffeeVariety, on_delete=models.PROTECT, related_name='orders')
    quantity = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.pk} — {self.coffee_variety.name} for {self.store.name}'

# One to One 

class coffeeCertificate(models.Model):
    coffee = models.OneToOneField(CoffeeVariety,on_delete=models.CASCADE,related_name='certificate')
    certificate_number=models.CharField(max_length=100)
    issued_date=models.DateTimeField(default=timezone.now)
    valid_untill = models.DateTimeField()

    def __str__(self):
        return f'Certificate for {self.coffee.name}'

  
