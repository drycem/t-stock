from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('urunler.urls')),
    # path('', include('react_frontend.urls')),
]
