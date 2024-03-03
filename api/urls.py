from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('registracija/', views.RegistrationView.as_view(), name='registration'),
    path('pretplate/', views.SubscriptionListView.as_view(), name='subscription-list'),
    path('pretplate/<int:pk>/', views.SubscriptionDetailView.as_view(), name='subscription-detail'),
    path('prijava/', CustomLoginView.as_view(), name='prijava'),
]
