from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('navedex.base.urls')),
    path('naver/', include('navedex.naver.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(
        path('__debug__/', include(debug_toolbar.urls))
    )
