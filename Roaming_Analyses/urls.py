"""
URL configuration for Roaming_Analyses project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from roaming_files import views
from django.conf.urls.static import static
from django.conf import settings
from roaming_files.views import roaming_in_stats, roaming_out_stats

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('RoamingIn/<int:pk>/', roaming_in_stats, name='roaming_in_stats'),
    path('RoamingOut/<int:pk>/', roaming_out_stats, name='roaming_out_stats'),
    path('django_plotly_dash/', include('django_plotly_dash.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
