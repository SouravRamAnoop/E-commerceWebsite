from django.urls import path

from . import views
from .views import BookList, BookView, BookCheckOutView, home, PaymentComplete, SearchResultsView, cart, add_to_cart, \
    remove_from_cart

urlpatterns= [
    path('',views.home, name='home'),
    path('about/',views.about, name='about'),
    path('contact/',views.contact, name='contact'),
    path('search/',SearchResultsView.as_view(),name='search'),
    path('booklist/',BookList.as_view(),name='books'),
    path('bookdetails/<int:pk>/',BookView.as_view(),name='details'),
    path('checkout/<int:pk>/',BookCheckOutView.as_view(),name='checkout'),
    path('complete/',PaymentComplete,name='complete'),
    path('cart/',cart,name='mycart'),
    path('cart/add/<int:book_id>/',add_to_cart,name="add_to_cart"),
    path('cart/remove/<int:book_id>/',remove_from_cart,name="remove_from_cart")
]