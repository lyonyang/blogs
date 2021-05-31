"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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

from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers
from quickstart import views

# 因为使用的是viewsets,所以使用路由器进行注册
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    # rest_framework自带的url,login与logout:
    #   - url(r'^login/$', login, login_kwargs, name='login'),
    #   - url(r'^logout/$', logout, name='logout'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]