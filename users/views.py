# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from rest_framework import generics, permissions,status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, UserProfileSerializer,RegisterSerializer, ChangePasswordSerializer
from rest_framework.views import APIView
from django.shortcuts import render, redirect, get_object_or_404
import json
from knox.views import LoginView as KnoxLoginView
from .models import UserProfile
import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters import FilterSet
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from .forms import UserForm
from .decorators import admin_hr_required, admin_only
        
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.permissions import IsAuthenticated
from .models import *
from .filters import OrderFilter
from django.forms import inlineformset_factory
# from .forms import OrderForm

# Create your views here.
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })        


class UserProfileAPI(APIView):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        profile_serializer = UserProfileSerializer(UserProfile)
        return Response(profile_serializer.data)


class PurchaseList(generics.ListAPIView):
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Purchase.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(purchaser__username=username)
        return queryset
# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email']
    ordering = ['username']
    


    
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'in_stock']


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('title_only'):
            return ['title']
        return super(CustomSearchFilter, self).get_search_fields(view, request)
    
    
class BookingsListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
    
    
class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)
    
    

@login_required(login_url="/login/")
def success(request):
    context = {}
    context['user'] = request.user
    return render(request, "auth/success.html", context)
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))
@login_required(login_url="/login/")
def employee_list(request):
    print(request.role)
    context = {}
    context['users'] = User.objects.all()
    context['title'] = 'Employees'
    return render(request, 'users/index.html', context)
@login_required(login_url="/login/")

def employee_details(request, id=None):
    context = {}
    context['user'] = get_object_or_404(User, id=id)
    return render(request, 'users/details.html', context)

@login_required(login_url="/login/")
@admin_only
def employee_add(request):
    context = {}
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        context['user_form'] = user_form
        if user_form.is_valid():
            u = user_form.save()    
            return HttpResponseRedirect(reverse('users_list'))
        else:
            return render(request, 'users/add.html', context)
    else:
        user_form = UserForm()
        context['user_form'] = user_form
        return render(request, 'users/add.html', context)
    
@login_required(login_url="/login/")
def users_edit(request, id=None):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()    
            return HttpResponseRedirect(reverse('users_list'))
        else:
            return render(request, 'users/edit.html', {"user_form": user_form})
    else:
        user_form = UserForm(instance=user)
        return render(request, 'users/edit.html', {"user_form": user_form})
    
@login_required(login_url="/login/")
def users_delete(request, id=None):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        return HttpResponseRedirect(reverse('users_list'))
    else:
        context = {}
        context['user'] = user
        return render(request, 'users/delete.html', context)
    
class ProfileUpdate(UpdateView):
    fields = ['designation', 'salary', 'picture']
    template_name = 'auth/profile_update.html'
    success_url = reverse_lazy('my_profile')
    def get_object(self):
        return self.request.user.profile
    
class MyProfile(DetailView):
    template_name = 'auth/profile.html'
    def get_object(self):
        return self.request.user.profile

    
class LogoutView(APIView):
    authentication_classes = (TokenAuthentication, )
    def post(self, request):
        django_logout(request)
        return Response(status=204)
    
class EmployeeFilter(FilterSet):
    is_active = filters.CharFilter('is_active')
    designation = filters.CharFilter('profile__designation')
    min_salary = filters.CharFilter(method="filter_by_min_salary")
    max_salary = filters.CharFilter(method="filter_by_max_salary")
    class Meta:
        model = User
        fields = ('is_active', 'designation', 'username',)
    def filter_by_min_salary(self, queryset, name, value):
        queryset = queryset.filter(profile__salary__gt=value)
        return queryset
    def filter_by_max_salary(self, queryset, name, value):
        queryset = queryset.filter(profile__salary__lt=value)
        return queryset
    
class EmployeeListView(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    # filter_fields = ('is_active', 'profile__designation', )
    filter_class = EmployeeFilter
    ordering_fields = ('is_active', 'username')
    ordering = ('username',)
    search_fields = ('username', 'first_name')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# def simpleCheckout(request):
# 	return render(request, 'users/simple_checkout.html')

# def store(request):
# 	products = Product.objects.all()
# 	context = {'products':products}
# 	return render(request, 'users/store.html', context)

# def checkout(request, pk):
# 	product = Product.objects.get(id=pk)
# 	context = {'product':product}
# 	return render(request, 'users/checkout.html', context)

# def paymentComplete(request):
#     body = json.loads(request.body)
#     print('BODY:', body)
#     product = Product.objects.get(id=body['productId'])
#     Order.objects.create(product=product)
#     return JsonResponse('Payment completed!', safe=False)


# # Search Api
# def home(request):
# 	orders = Order.objects.all()
# 	customers = Customer.objects.all()
# 	total_customers = customers.count()
# 	total_orders = orders.count()
# 	delivered = orders.filter(status='Delivered').count()
# 	pending = orders.filter(status='Pending').count()

# 	context = {'orders':orders, 'customers':customers,
# 	'total_orders':total_orders,'delivered':delivered,
# 	'pending':pending }

# 	return render(request, 'users/dashboard.html', context)

# def products(request):
# 	products = Product.objects.all()
# 	return render(request, 'users/products.html', {'products':products})

# def customer(request, pk_test):
# 	customer = Customer.objects.get(id=pk_test)
# 	orders = customer.order_set.all()
# 	order_count = orders.count()
# 	myFilter = OrderFilter(request.GET, queryset=orders)
# 	orders = myFilter.qs 
# 	context = {'customer':customer, 'orders':orders, 'order_count':order_count,
# 	'myFilter':myFilter}
# 	return render(request, 'users/customer.html',context)


# def createOrder(request, pk):
# 	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
# 	customer = Customer.objects.get(id=pk)
# 	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
# 	if request.method == 'POST':
# 		formset = OrderFormSet(request.POST, instance=customer)
# 		if formset.is_valid():
# 			formset.save()
# 			return redirect('/')

# 	context = {'form':formset}
# 	return render(request, 'users/order_form.html', context)

# def updateOrder(request, pk):
# 	order = Order.objects.get(id=pk)
# 	form = OrderForm(instance=order)

# 	if request.method == 'POST':
# 		form = OrderForm(request.POST, instance=order)
# 		if form.is_valid():
# 			form.save()
# 			return redirect('/')

# 	context = {'form':form}
# 	return render(request, 'users/order_form.html', context)

# def deleteOrder(request, pk):
# 	order = Order.objects.get(id=pk)
# 	if request.method == "POST":
# 		order.delete()
# 		return redirect('/')

# 	context = {'item':order}
# 	return render(request, 'users/delete.html', context)
