from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('report/', views.report, name='report'),
    path('api/html_encode/', views.api_html_encode, name='api_html_encode'),
    path('api/sql_search/', views.api_sql_search, name='api_sql_search'),
    path('api/subscribe/', views.api_subscribe, name='api_subscribe'),
]
