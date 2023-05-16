from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from books.views import pageNotFound
from .settings import MEDIA_ROOT, MEDIA_URL, DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

handler404 = pageNotFound