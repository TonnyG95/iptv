from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('registracija/', views.registracija, name='registracija'),
    path('prijava/', views.prijava, name='prijava'),
    path('', views.dashboard, name='dashboard'),
    path('preplate/', views.prikaz_pretplata, name='prikaz_pretplata'),
    path('preplate/<int:pretplata_id>/', views.placanje_pretplate, name='placanje_pretplate'),
    path('dashboard/lista-preplata/', views.lista_preplata, name='lista_preplata'),
    path('dashboard/lista-kanala/', views.lista_kanala, name='lista_kanala'),
    path('dashboard/balance/', views.balance, name='balance'),
    path('dashboard/podrska/', views.podrska, name='podrska'),
    path('dashboard/promijeni-status/<int:user_subscription_id>/<str:new_status>/', views.promijeni_status_preplate, name='promijeni_status_preplate'),
    path('dashboard/kupi-pretplatu/', views.kupi_pretplatu, name='kupi_pretplatu'),
    path('dashboard/produzi-preplatu/<int:pretplata_id>/', views.produzi_pretplatu, name='produzi_pretplatu'),
    path('kontakt/', views.kontakt_forma, name='kontakt_forma'),
    path('dashboard/postavke/', views.postavke, name='postavke'),
    path('paypal_payment/', views.paypal_payment, name='paypal_payment'),
    path('paypal/return/', views.paypal_return, name='paypal_return'),
    path('paypal/cancel/', views.paypal_cancel, name='paypal_cancel'),
    path('odjava/', auth_views.LogoutView.as_view(next_page='prijava'), name='odjava'),
    path('provjera-preplata/', views.provjera_preplata),
    path('update_m3u_status/', views.update_m3u_status, name='update_m3u_status'),
    

]
