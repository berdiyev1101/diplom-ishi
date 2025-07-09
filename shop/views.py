from itertools import product

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth import logout, authenticate,login

from shop.forms import SignUpForm, SignInForm, CommentForm
from shop.models import *


class Index(ListView):
    model = Category
    context_object_name = "data"
    template_name = "shop/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context["subcategories"] = SubCategory.objects.all()
        context["offers"] = Offer.objects.all()
        context["vendors"] = Vendor.objects.all()
        context["products"] = Product.objects.all()
        context["featured_products"] = Product.objects.all()[:4]
        context["best_products"] = Product.objects.all()[4:7]
        context["blogs"] = LatestBlog.objects.all()
        return context

class ProductByCategory(ListView):
    model = Product
    context_object_name = "products"
    template_name = "shop/category.html"
    paginate_by = 2

    def get_queryset(self):
        category = Category.objects.get(pk=self.kwargs['pk'])
        products = Product.objects.filter(category=category)
        sort_field = self.request.GET.get("sort")
        price_field = self.request.GET.getlist("price")
        area_field = self.request.GET.getlist("sale")
        if sort_field:
            products = products.order_by(sort_field)

        if price_field:
            price_choices = {
                '0-100':(0,100),
                '100-200':(100,200),
                '200-300':(200,300),
                '300-400':(300,400),
            }
            price_list = [price_choices[price] for price in price_field if price in price_choices]
            if price_list:
                products = products.filter(
                    price__gte=min(price[0] for price in price_list),
                    price__lte=max(price[1] for price in price_list)
                )

        if area_field:
            products = products.filter(area__in=area_field)
        return products

class ProductDetail(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "shop/detail.html"
    form_class = CommentForm()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(pk=self.kwargs['pk'])
        products = Product.objects.all()
        data = []
        i = 0
        while i <= 8:
            from random import randint
            random_product = products[randint(0,len(products)-1)]
            if not random_product in data:
                data.append(random_product)
                i += 1
        context['products'] = data
        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(product=product).order_by("-created_at")
        return context

def signup(request):
    form = SignUpForm(data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect("index")
    context = {
        "title":"Sign Up",
        "form":form
    }
    return render(request,"shop/signup.html",context)

def signin(request):
    form = SignInForm(data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(request, username=email, password=password)
            if user:
                login(request,user)
                return redirect("index")
    context = {
        "title":"Sign In",
        "form":form
    }
    return render(request,"shop/signin.html",context)

def signout(request):
    logout(request)
    return redirect("signin")

def contact(request):
    success = False
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        Contact.objects.create(name=name, email=email, subject=subject, message=message)
        success = True
    context = {
        "title":"Contact",
        "success":success
    }
    return render(request,"shop/contact.html", context)

class LikeList(ListView):
    model = Like
    template_name = "shop/like.html"
    context_object_name = "products"

    def get_queryset(self):
        user = self.request.user
        likes = Like.objects.filter(user=user)
        products = [like.product for like in likes]
        return products

def user_like(request,pk):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    product = Product.objects.get(pk=pk)
    if user:
        user_products = Like.objects.filter(user=user)
        if product in [like.product for like in user_products]:
            product_like = Like.objects.filter(user=user,product=product)
            product_like.delete()
        else:
            Like.objects.create(user=user, product=product)
    next_page = request.META.get("HTTP_REFERER","index")
    return redirect(next_page)

def basket(request):
    basket_products = Basket.objects.filter(user=request.user)
    total_price = sum([item.get_total_price() for item in basket_products])
    total_sale = sum([item.get_total_sale() for item in basket_products])
    total_quantity = sum([item.quantity for item in basket_products])
    sale = total_price - total_sale
    context = {
        "title":"Basket",
        "products":basket_products,
        "total_price":total_price,
        "total_sale":total_sale,
        "total_quantity":total_quantity,
        "sale":sale
    }
    return render(request,"shop/basket.html",context)

def basket_add(request,pk):
    product = get_object_or_404(Product,pk=pk)
    basket_product, create = Basket.objects.get_or_create(product=product, user=request.user)
    if not create:
        basket_product.quantity += 1
        basket_product.save()
    next_page = request.META.get("HTTP REFERER","index")
    return redirect(next_page)

def basket_update(request,pk):
    product = get_object_or_404(Basket, pk=pk, user=request.user )
    if request.method == "POST":
        quantity = int(request.POST.get("quantity",1))
        if quantity > 0:
            product.quantity = quantity
            product.save()
        else:
            product.delete()
    return redirect("basket")

def basket_remove(request,pk):
    product = get_object_or_404(Basket, pk=pk, user=request.user)
    product.delete()
    return redirect("basket")

def add_comment(request,pk):
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.product = Product.objects.get(pk=pk)
        comment.save()
    else:
        pass
    return redirect("detail",pk)

class ProductSearch(ListView):
    model = Product
    context_object_name = "products"
    template_name = "shop/category.html"

    def get_queryset(self):
        word = self.request.GET.get('q')
        products = Product.objects.filter(Q(title__icontains=word))
        return products

class IndexSearch(ListView):
    model = Product
    context_object_name = "products"
    template_name = "shop/index.html"

    def get_queryset(self):
        word = self.request.GET.get('q')
        products = Product.objects.filter(Q(title__icontains=word))
        return products

class Location(TemplateView):
    template_name = "shop/location.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address'] = "Toshkent shahri, Mustaqillik ko'chasi, 10-uy"
        return context

class MyAccount(TemplateView):
    template_name = "shop/my_account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(user=self.request.user).order_by("-created_at")
        return context


