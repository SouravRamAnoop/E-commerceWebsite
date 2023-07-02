from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Book, Order, Cart, CartItem
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    return render(request,'index.html')

class SearchResultsView(ListView):
    model = Book
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(
            Q(title=query) | Q(author=query)

        )

class BookList(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'booklist.html'

class BookView(DetailView):
    model = Book
    context_object_name = 'details'
    template_name = 'bookdetails.html'

class BookCheckOutView(DetailView):
    model = Book
    context_object_name = 'checkout'
    template_name = 'checkout.html'

def PaymentComplete(request,pk):
    product=Book.objects.get(id=pk)
    Order.objects.create(
        product=product
    )
    return JsonResponse('Payment completed', safe=False)

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

@login_required
def cart(request):
    cart_qs = Cart.objects.filter(user = request.user)
    if cart_qs.exists():
        cart_obj = cart_qs.first()
        cart_items = CartItem.objects.filter(cart=cart_obj)

    else:
        cart_obj = None
        cart_items = []

    context = {
        'cart':cart_obj,
        'cart_items':cart_items
    }
    return render(request,'mycart.html',context)

@login_required
def add_to_cart(request,book_id):
    book= get_object_or_404(Book,id=book_id)
    cart_qs = Cart.objects.filter(user = request.user)
    if cart_qs.exists():
        cart_obj = cart_qs.first()

    else:
        cart_obj = Cart.objects.create(user = request.user,total_price=Decimal('0.00'))
    cart_item ,created = CartItem.objects.get_or_create(book=book,cart=cart_obj)
    if not created:
        cart_item.quantity +=1
        cart_item.save()
    cart_obj.total_price += Decimal(str(book.price))
    cart_obj.save()
    return redirect('mycart')

@login_required()
def remove_from_cart(request,book_id):
    book = get_object_or_404(Book,id=book_id)
    cart_qs=Cart.objects.filter(user=request.user)
    if cart_qs.exists():
        cart_obj = cart_qs.first()
        cart_item_qs = CartItem.objects.filter(book=book,cart=cart_obj)
        if cart_item_qs.exists():
            cart_item = cart_item_qs.first()
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
            cart_obj.total_price -= Decimal(str(book.price))
            cart_obj.save()
    return redirect('mycart')
