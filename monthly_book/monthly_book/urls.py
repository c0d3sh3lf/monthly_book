"""monthly_book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

api_base_url = "api/v1/"

urlpatterns = [
    path('', include(('mbook.urls', 'mbook'), namespace='mbook')),
    path('umanage/', include(('user_management.urls', 'user_management'), namespace='user_management')),
    path(api_base_url, include(('mbook.api_urls', 'mbook_api'), namespace='mbook_api')),
    path(api_base_url + 'umanage/', include(('user_management.api_urls', 'user_management_api'), namespace='user_management_api')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
