from django.db import models
from django.urls import reverse
    
# Create your models here.
class ProgramDetail(models.Model):
    time1=models.CharField(max_length=255,blank=True)
    description1=models.TextField(blank=True)
    time2=models.CharField(max_length=255,blank=True)
    description2=models.TextField(blank=True)
    time3=models.CharField(max_length=255,blank=True)
    description3=models.TextField(blank=True)
    time4=models.CharField(max_length=255,blank=True)
    description4=models.TextField(blank=True)
    time5=models.CharField(max_length=255,blank=True)
    description5=models.TextField(blank=True)
    time6=models.CharField(max_length=255,blank=True)
    description6=models.TextField(blank=True)
   

class Program(models.Model):
    name=models.CharField(max_length=255,unique=True)
    slug=models.SlugField(max_length=255,unique=True)
    program_details=models.ForeignKey(ProgramDetail,on_delete=models.CASCADE)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    promotion_price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to="program",blank=True)
    available=models.BooleanField(default=True)
    promotion=models.BooleanField(default=True)
    create=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('program_details',args=[self.slug])

    def get_book_url(self):
        return reverse('program_book',args=[self.slug]) 


    def __str__(self):
        return self.name

class Order(models.Model):
    name=models.CharField(max_length=255,blank=True)
    address=models.CharField(max_length=255,blank=True)
    city=models.CharField(max_length=255,blank=True)
    postcode=models.CharField(max_length=255,blank=True)
    total=models.DecimalField(max_digits=10,decimal_places=2)
    email=models.EmailField(max_length=250,blank=True)
    token=models.CharField(max_length=255,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    program=models.CharField(max_length=250)
    checkin_date=models.DateTimeField(auto_now_add=True)
    adults=models.DecimalField(max_digits=10,decimal_places=2)
    children=models.DecimalField(max_digits=10,decimal_places=2)
    def __str__(self):
        return str(self.id)      