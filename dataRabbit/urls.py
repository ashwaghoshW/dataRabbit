

from django.contrib import admin
from django.urls import path, include
from info import views
from dashboard import Dashboard,urls
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('blog/', include('blog.urls')),
    # path('tinymce/', include('tinymce.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
