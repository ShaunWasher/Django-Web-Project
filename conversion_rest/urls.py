from django.urls import path
from . import views

urlpatterns = [
    path('£/£/', views.same),
    path('£/$/', views.GBP_USD),
    path('£/€/', views.GBP_Euro),
    path('$/£/', views.USD_GBP),
    path('$/$/', views.same),
    path('$/€/', views.USD_Euro),
    path('€/£/', views.Euro_GBP),
    path('€/$/', views.Euro_USD),
    path('€/€/', views.same),
]