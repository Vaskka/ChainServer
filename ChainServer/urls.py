"""ChainServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

import Transfer.views

transfer_regex = r'^transfer/\?a_user_phone=[0-9]{11}&b_user_phone=[0-9]{11}&money=.*$'
request_regex = r'^request/\?user_phone=[0-9]{11}&status=[a-z]+$'
complete_regex = r'^complete/\?user_phone=[0-9]{11}&status=(success|fail)$'


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'transfer/', view=Transfer.views.do_transfer),
    url(r'request/', view=Transfer.views.do_common_query),
    url(r'complete/', view=Transfer.views.do_complete_verify)
]
