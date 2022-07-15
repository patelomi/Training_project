from statistics import mode
from django.db import models
from django.db import transaction
# Create your models here.
class CustomerGroup(models.Model):
    choice = (
        ('Yes','Yes'),
        ('No','No'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(("Name"), max_length=60, unique=True, null=False)
    isdefault = models.CharField(("Is Default"), max_length=10, choices=choice, default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self,*args,**kwargs):
        if self.isdefault == "No":
            return super(CustomerGroup,self).save(*args,**kwargs)
        with transaction.atomic():
            CustomerGroup.objects.filter(
                isdefault="Yes").update(isdefault="No")
            return super(CustomerGroup,self).save(*args,**kwargs)

    def __str__(self):
        return self.name

class Customer(models.Model):
    choice = (
        ('Yes','Yes'),
        ('No','No'),
    )
    cid = models.AutoField(primary_key=True)
    group = models.ForeignKey(CustomerGroup, on_delete=models.SET_NULL, null=True)
    firstname = models.CharField(("First Name"), max_length=200, null=False)
    lastname = models.CharField(("Last Name"), max_length=200, null=False)
    profileimg = models.ImageField(("Profile Image"), upload_to="images/", null=True)
    email = models.EmailField(("Email"), max_length=40, null=False)
    emailvarifaction = models.CharField(("Email Varifaction"), max_length=10, choices=choice, default=False, null=True)
    emailvarificationdate = models.DateTimeField(("Varification Date"), null=True)
    phoneno = models.IntegerField(("Phone Number"), null=False)
    password = models.CharField(("Password"), max_length=200, null=False)
    confirmpassword = models.CharField(("Confirm Password"), max_length=200, null=False)
    code = models.CharField(max_length=10, default=0, null=True)
    time = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.cid)


class State(models.Model):
    stateid = models.AutoField(primary_key=True)
    satatename = models.CharField(max_length=200, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.satatename

class City(models.Model):
    cityid = models.AutoField(primary_key=True)
    cityname = models.CharField(max_length=200, null=False, unique=True)
    statename = models.ForeignKey(State, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.cityname

class Address(models.Model):
    choice = (
        ('Yes','Yes'),
        ('No','No'),
    )
    aid = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, blank=True)
    streetname = models.CharField(max_length=200)
    houseno = models.CharField(max_length=200)
    unitno = models.CharField(max_length=200)
    postalcode = models.IntegerField(null=False)
    tag = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=False)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=False)
    isdefault = models.CharField(("Is Default"), max_length=10, choices=choice, default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self,*args,**kwargs):
        if self.isdefault == "No":
            return super(Address,self).save(*args,**kwargs)
        with transaction.atomic():
            Address.objects.filter(
                isdefault="Yes").update(isdefault="No")
            return super(Address,self).save(*args,**kwargs)

    def __str__(self):
        return self.name + str(self.customer)