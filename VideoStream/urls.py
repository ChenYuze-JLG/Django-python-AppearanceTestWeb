"""VideoStream URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from app import views
from django.urls import re_path as url
from django.conf.urls import include

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('app/index/',views.index),
    path('app/login/', views.myLogin),
    path('app/register/', views.addUser),
    url(r'^captcha/', include('captcha.urls')),
    path('app/video/ajax/', views.processAjax),
    path('app/history/', views.history),
    path('app/history/ajax/', views.processHistory),
    path('app/history/rank/', views.showRank),
    path('app/register/ajax/<str:username>', views.usernameAjax),
    path('app/logout/', views.myLogout),
    path('app/help/', views.help),
    path('app/history/DeleteUserById/', views.DeleteUserById),

]
