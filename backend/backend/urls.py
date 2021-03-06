"""backend URL Configuration

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
from django.urls import path
import external_api
import upload_api
import apis
import authentication
import history

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'query/<str:api>', external_api.query),
    path(r'upload/', upload_api.upload),
    path(r'api/', apis.get),
    path(r'auth/', authentication.get_auth_uri),
    path(r'code/', authentication.consume_auth_code),
    path(r'refresh/', authentication.refresh_tokens),
    path(r'history/', history.get)
]
