from django.urls import path
from Block import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('demo/',views.demo,name='demo'),
    
]