"""yangw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.urls import path
from . import views
app_name='yangw0123'
urlpatterns = [
    path('login/',views.login,name="login"),
    path('test/',views.test,name="test"),
    path('container_get/',views.coantainer_get,name="container_get"),
    path('container_main/',views.container_main,name='container_main'),
    path('container_create_1/',views.container_create_1,name='container_create_1'),
    path('container_create/',views.container_create,name='container_create'),
    path('container_delete/<name>',views.container_delete,name='container_delete'),
    path('container_delete_1/<name>', views.container_delete_1, name='container_delete_1'),
    path('container_success/',views.container_success,name='container_success'),
    path('word_list/<name>/',views.word_list,name='word_list'),
    path('object/<name>/<objname>',views.object,name='object'),
    path('object_delete/<name>/<objname>',views.object_delete,name='object_delete'),
    path('object_delete_1/<name>/<objname>',views.object_delete_1,name='object_delete_1'),
    path('uploadObject/<name>',views.uploadObject,name='uploadObject'),
    path('uploadObject_1/<name>',views.uploadObject_1,name='uploadObject_1'),
    path('downloadObject/<name>/<objname>',views.downloadObject,name='downloadObject'),
    path('downloadObject_1/<name>/<objname>',views.downloadObject_1,name='downloadObject_1'),
]
