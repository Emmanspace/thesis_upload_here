from django.db import models
from django.template import defaultfilters
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
# from db_connection import db
from djongo import models

# modify
from django.contrib.auth.models import User,  BaseUserManager, PermissionsMixin, Permission

# Create your models here.

# commented
class Notification(models.Model):
    notification = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-notification',)
    
    def created_at_formatted(self):
        return defaultfilters.date(self.created_at, 'M d, Y')

class Category(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        ordering = ('title',)


class History(models.Model):
    category = models.ForeignKey(Category, related_name='jobs', on_delete=models.CASCADE)
    intent = models.CharField(max_length=255)
    announcement = models.TextField()
    start = models.TimeField(auto_now_add=True)
    end = models.TimeField()
    duration = models.TimeField(max_length=255)
    date_at = models.DateTimeField(auto_now_add=True)
    Total_parking_Slots = models.IntegerField(default=50)
    Vehicles_Parked = models.IntegerField(default=0)
    Available_slots = models.IntegerField(default=50)

    class Meta:
        ordering=('-date_at',)

    def date_formatted(self):
        return defaultfilters.date(self.date_at, 'M d, Y')
    
# end of commented

# commented
class totalSlots(models.Model):
    total_slots = models.IntegerField()
    class Meta:
        ordering=('-total_slots',)

class availableSlots(models.Model):
    available_slots = models.IntegerField()
    class Meta:
        ordering=('-available_slots',)

class parkingSlots(models.Model):
    parking_slots = models.IntegerField()
    class Meta:
        ordering=('-parking_slots',)


# for jairo's db
class real_time(models.Model):
    confidence = models.FloatField()
    plate = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    class Meta:
        ordering=('-plate',)
    
    def date_formatted(self):
        return defaultfilters.date(self.date, 'M d, Y')
# end of commented

# added
# for test run
class Departments(models.Model):
    DepartmentId = models.AutoField(primary_key=True)
    DepartmentName = models.CharField(max_length=500)
# end of testrun
# end of added
    
# for historytab
class historytab(models.Model):
    intent = models.CharField(max_length=255)
    start = models.TimeField(auto_now_add=True)
    end = models.TimeField(auto_now_add=True)
    duration = models.TimeField(auto_now_add=True)
    date_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-date_at',)

    def date_formatted(self):
        return defaultfilters.date(self.date_at, 'M d, Y')
    
# for change/update of user
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    plate = models.CharField(max_length=255, default='')

    def __str__ (self):
        return f"{self.first_name} {self.last_name}'s Profile"
# end of change/update


# for authentication
class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, plate, password=None): #added : first_name, last_name, plate
        if not email:
            raise ValueError('The Email field must be set')
        # email = self.normalize_email(email)
        if not username:
            raise ValueError('user must have username')
        
        user = self.model(
            email=self.normalize_email(email),
            username = username,
            first_name= first_name,
            last_name= last_name,
            plate = plate
        )
        # username = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, first_name, last_name, plate,password=None,): #added : first_name, last_name, plate
        user = self.create_user(
            email=self.normalize_email(email),
            username = username,
            password=password,

        )
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        return user
    
    
class User(User, PermissionsMixin):
    user_email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    user_username = models.CharField(max_length=150, unique=True)
    user_is_active =models.BooleanField(default=True)
    user_is_staff = models.BooleanField(default=False)
    user_first_name = models.CharField(max_length=255, default='') #added
    user_last_name = models.CharField(max_length=255, default='') #added
    user_plate = models.CharField(max_length=255, default='') #added

    # user_email = models.EmailField(unique=True)
    # user_username = models.CharField(max_length=255, unique=True)
    # user_first_name = models.CharField(max_length=30, blank=True)
    # user_last_name = models.CharField(max_length=30, blank=True)
    # user_is_active = models.BooleanField(default=True)
    # user_is_staff = models.BooleanField(default=False)
    # user_date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    # users_permissions = models.ManyToManyField(
    #     Permission,
    #     verbose_name='user permissions',
    #     blank=True,
    #     related_name='custom_user_permissions'
    # )
    # class Meta:
    #     verbose_name = 'user'
    #     verbose_name_plural = 'users'

    def __str__(self):
        return self.email
# end of authentication

# 4-23
# class userEdit(models.Model):
#     _id = models.BigAutoField(primary_key=True)
#     # id = models.AutoField(primary_key=True)
#     password = models.CharField(max_length=255)
#     last_login = models.DateTimeField(auto_now_add=False)
#     is_superuser = models.BooleanField(default=False)
#     username = models.CharField(max_length=200, blank=False, default='')
#     first_name =  models.CharField(max_length=200, blank=False, default='')
#     last_name = models.CharField(max_length=200, blank=False, default='')
#     email = models.EmailField()
#     is_staff = models.BooleanField(default=False)
#     is_active= models.BooleanField(default=True)
#     date_joined = models.DateTimeField()
# 4-23


# # @admin.register(User)
# class AccountAdmin(UserAdmin):
#     list_display = (
#         'username',
#         'first_name',
#         'last_name',
#         'email',
#         'date_joined',
#         'last_login',
#         'is_staff',
#     )
#     search_fields = ('email',)
#     readonly_fields=('date_joined', 'last_login')
#     fieldsets = (
#         (None, {"fields": ("email", "password")}),
#         (_("Personal info"), {"fields": ("first_name", "last_name")}),
#         (
#             _("Permissions"),
#             {
#                 "fields": (
#                     "is_active",
#                     "is_staff",
#                     "is_superuser",
#                     "company",
#                     "groups",
#                     "user_permissions",
#                 ),
#             },
#         ),
#         (_("Important dates"), {"fields": ("last_login", "date_joined")}),
#     )
#     add_fieldsets = (
#             (
#                 None,
#                 {
#                     'classes': ('wide',),
#                     'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
#                 },
#             ),
#         )


# for custom user admin
# class NewUser(AbstractUser):
#     user_first_name = models.CharField(max_length=200,null=True)
#     user_last_name = models.CharField(max_length=200, null=True)
#     user_plate = models.CharField(max_length=200, null=True)
#     user_email = models.EmailField(max_length=200, null=True)



class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email is not given.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff = True")

        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser = True")
        return self.create_user(email, password, **extra_fields)


