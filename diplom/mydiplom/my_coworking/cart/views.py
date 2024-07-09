from itertools import product

from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from . import models

from datetime import datetime, timedelta

import stripe



def product_list(request):
    products = Product.objects.all()
    return render(request, 'cart/index.html', {'products': products})

def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product,
                                                    user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart:view_cart')

def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart:view_cart')


def first_page(request):
    template_name = 'cart/search_results.html'
    all_time = ['08:00', '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00', '15:00',
                '16:00', '17:00', '18:00', '19:00',]

    yesterday = datetime.today()
    min_day_value = yesterday.strftime("%Y-%m-%d")

    if request.GET.get('date') is None:
        dict_obj = {'min_day_value':min_day_value,
                'all_time':all_time,
                'step_1': True,
                'step': 'Шаг 1',
        }
        return render(request, 'cart/select_date.html', dict_obj)
    else:
        appointments = CartItem.objects.filter(order_day=request.GET.get('date')).all()
        for obj in appointments:
            all_time.remove(obj.order_time.strftime("%H:%M"))
        dict_obj = {'min_day_value':min_day_value,
                    'all_time':all_time,
                    'step_1': False,
                    'step_2': True,
                    'step': 'Шаг 2',
                    'choised_day': request.GET.get('date'),
                    }
    return render(request, 'cart/select_date.html', dict_obj)


def thanks_page(request):
    if request.POST:
        day = request.POST['day']
        time = request.POST['time']
        element = CartItem.objects.filter(
                        user=request.user,
                        order_day = day,
                        order_time = time,
                        )
        element.save()

        total_price = sum(item.product.price * item.quantity for item in element)
        return render(request, 'cart/cart.html', {'element': element, 'total_price': total_price})





def select(request):
    product = request.GET.get('product')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    products = CartItem.objects.filter(product__icontains=product, order_day__lte=end_date, order_time__gte=start_date)
    context = {
        'products': products
    }
    return render(request, 'select_date.html', context)

class HomePageView(TemplateView):
    template_name = 'search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_by = self.request.GET.get('search_by')
        query = self.request.GET.get('query')
        search_message = "All Product"
        if search_by in ['name'] and query:
            if search_by == 'name':
                search_message = f'Searching for "name" by {query}'
                products = models.Product.objects.filter(name=query)
                context['products'] = products
                return context
        context['search_message'] = search_message
        context['products'] = models.Product.objects.all()
        return context


class SearchResultsView(ListView):
    model = Product
    template_name = 'cart/search_results.html'

    def get_queryset(self):  # новый
        query = self.request.GET.get('q')
        search_vector = SearchVector('description', weight='B') + SearchVector('name', weight='A')
        search_query = SearchQuery(query)
        return (self.model.objects.annotate(rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.3).order_by('-rank'))



def home(request):
    return HttpResponse('Hello, World!')



from datetime import datetime, timedelta


def get_available_dates(request):
    """
    Функция возвращает список доступных дат и времени для заказа.
    """
    # Получаем все существующие заказы
    cart_items = CartItem.objects.all()

    # Создаем словарь, где ключ - дата, а значение - список занятых временных интервалов
    occupied_slots = {}
    for item in cart_items:
        date = item.order_day
        time = item.order_time
        if date not in occupied_slots:
            occupied_slots[date] = []
        occupied_slots[date].append(time)

    # Генерируем список доступных дат и времени
    available_dates = []
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=7)  # Ограничиваем диапазон на 7 дней
    while start_date <= end_date:
        available_times = ['08:00', '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00', '15:00',
                '16:00', '17:00', '18:00', '19:00',]
        if start_date not in occupied_slots:
            available_dates.append((start_date, available_times))
        else:
            occupied_times = occupied_slots[start_date]
            for time in available_times:
                if time not in occupied_times:
                    available_dates.append((start_date, [time]))
        start_date += timedelta(days=1)

    return available_dates



from .models import Product


def search_products(request):
    """
    Функция выполняет поиск продуктов по названию.
    """
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, 'cart/products.html', {'products': products})

def order_page(request):
    if request.method == 'POST':
        order_day = request.POST['order_day']
        order_time = request.POST['order_time']
        # Обработка данных заказа и сохранение в базу данных
        cart_item = CartItem.objects.create(
            product=product,
            user=request.user,
            order_day=order_day,
            order_time=order_time,
        )
        return redirect('cart')
    else:
        cart_item = CartItem.objects.filter(user=request.user).first()
        return render(request, 'cart/order.html', {'cart_item': cart_item})



def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user, payment_status="unpaid")
    total_price = sum(item.get_total_price() for item in cart_items)

    if request.method == "POST":
        for item in cart_items:
            client_secret = item.create_payment_intent()
            context = {
                "client_secret": client_secret,
                "cart_items": cart_items,
                "total_price": total_price,
            }
            return render(request, "checkout.html", context)

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
    }
    return render(request, "checkout.html", context)

def handle_payment(request):
    payment_intent_id = request.POST.get("payment_intent_id")
    payment_status = request.POST.get("payment_status")

    try:
        cart_item = CartItem.objects.get(payment_intent_id=payment_intent_id)
        cart_item.update_payment_status(payment_status)
        return redirect("cart")
    except CartItem.DoesNotExist:
        return redirect("checkout")