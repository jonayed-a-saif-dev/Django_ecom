from django.conf import settings #adding by saif
from django.contrib import admin
from django.urls import path,include  
from django.conf.urls.static import static #adding by saif


urlpatterns  = [
    path('admin/', admin.site.urls),
    path('', include('product.urls')),#adding by saif
    path('', include('user_account.urls')),#adding by saif
]

#adding by saif
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
