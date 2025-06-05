# residents/urls.py

from django.urls import path
from . import views

# Define the URL patterns for the residents app
# These paths are relative to the '/residents/' path defined in the project's urls.py
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_resident, name='add_resident'),
    path('<int:resident_id>/', views.resident_detail, name='resident_detail'),
    path('<int:resident_id>/edit/', views.edit_resident, name='edit_resident'),
    path('<int:resident_id>/delete/', views.delete_resident, name='delete_resident'),
    path('transactions/', views.transactions_list_view, name='transactions_list'),
    path('reporting/', views.reporting_page_view, name='reporting_page'),
    path('ajax/search_residents/', views.search_residents_ajax, name='search_residents_ajax'),
    path('ajax/get-officials/', views.get_barangay_officials_api, name='get_barangay_officials_api'),
]
