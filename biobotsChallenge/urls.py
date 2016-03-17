"""biobotsChallenge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^biobotsApp/', include('biobotsApp.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', 'biobotsApp.views.login_user'), 
    url(r'^submit/$', 'biobotsApp.views.submit_user'),
    url(r'^login/view_print_result/$', 'biobotsApp.views.view_print_result'),
    url(r'^login/view_pressure_result/$', 'biobotsApp.views.view_pressure_result'),
    url(r'^login/view_crosslinking_result/$', 'biobotsApp.views.view_crosslinking_result'),
    url(r'^login/view_layernum_result/$', 'biobotsApp.views.view_layernum_result'),
    url(r'^login/view_layerheight_result/$', 'biobotsApp.views.view_layerheight_result')
 ]


