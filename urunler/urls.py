from django.urls import path

from . import views
urlpatterns = [
    path('api/', views.UrunlerListCreate.as_view(), name='api-list-create'),
    path('api/<int:pk>/', views.UrunlerUpdate.as_view(), name='api-update'),
    path('', views.home, name='urunler-home'),
    path('urunler/', views.UrunlerListView.as_view(), name='urunler-list'),
    path('<int:pk>/', views.UrunlerDetailView.as_view(), name='urunler-detail'),
    path('<int:pk>/update/', views.UrunlerUpdateView.as_view(), name='urunler-update'),
    path('search/', views.urunlerSearchView, name='urunler-search'),
    path('<int:urun_id>/buy/', views.urunlerBuy, name='urunler-buy'),
    path('<int:urun_id>/sell/', views.urunlerSell, name='urunler-sell'),
    path('islemler/', views.IslemlerListView.as_view(), name='islemler-list'),
]
