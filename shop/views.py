from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth import logout, authenticate,login

from shop.forms import SignUpForm, SignInForm
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
        return products


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






