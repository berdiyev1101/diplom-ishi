from django.contrib.auth.models import BaseUserManager,AbstractUser
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Email must be fill")
        email = self.normalize_email(email=email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault("is_staff",True)
        kwargs.setdefault("is_superuser",True)
        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must be is_staff TRUE")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must be is_superuser TRUE")
        return self.create_user(email=email, password=password, **kwargs)

class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

class Category(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class SubCategory(models.Model):
    title = models.CharField(max_length=100)
    info = models.TextField(max_length=250)
    image = models.ImageField(upload_to="images/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="subcategory")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "SubCategory"
        verbose_name_plural = "SubCategories"


class Offer(models.Model):
    image = models.ImageField(upload_to="images/")


class Vendor(models.Model):
    image = models.ImageField(upload_to="images/")
    title = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    sale = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    description = models.TextField(default="The description is not available")
    quantity = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_first_name(self):
        if self.images:
            try:
                return self.images.first().image.url
            except:
                return "https://avatars.mds.yandex.net/i?id=cb7631da68336d1560b26115134c1765f341e9f7-5248434-images-thumbs&n=13"
        return "https://avatars.mds.yandex.net/i?id=cb7631da68336d1560b26115134c1765f341e9f7-5248434-images-thumbs&n=13"

    def __str__(self):
        return self.title

class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="images/")

    class Meta:
        verbose_name = "Gallery"
        verbose_name_plural = "Galleries"

    def __str__(self):
        return self.product.title

class LatestBlog(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to="images")

    def __str__(self):
        return self.title


