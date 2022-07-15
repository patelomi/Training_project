"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
# from django.contrib.staticfiles.utils import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from Customer import views

urlpatterns = [
    path('admin/login/', auth_views.LoginView.as_view(template_name = 'admin/login.html'),name = 'login'),
    path('admin/', admin.site.urls),
    path('',include('Pages.urls')),
    path('',include('Theame.urls')),
    path('delete/',views.deletedata,name='delete'),
    path('edit/',views.editdata,name='edit'),
    path('emailvarification/',views.emailvarification,name='emailvarification'),
    path('',include('Block.urls')),
    # path('email/',views.email,name='email')
    # path('/',views.index,name='index')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
