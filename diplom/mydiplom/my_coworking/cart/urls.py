from django.urls import path
from . import views
from .views import SearchResultsView, HomePageView

app_name = 'cart'

urlpatterns = [
	path('', views.product_list, name='product_list'),
	path('index/', views.product_list, name='catalog'),
	path('home/', views.home, name='home'),

	path('search_results/', SearchResultsView.as_view(), name='search_results'),
	path('search_results/', HomePageView.as_view(), name='search_results'),
    path('products/', views.search_products, name='search_product'),

	path('order/', views.order_page, name='order_date'),
	path('select_date/', views.get_available_dates, name='select_date'),
    path('select_date/', views.select, name='select_date'),

	path('cart/', views.view_cart, name='view_cart'),
	path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
	path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
