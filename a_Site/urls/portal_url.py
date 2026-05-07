from django.urls import path

from a_Site.views import index


app_name = 'portal'

urlpatterns = [
    path('<path:url>/', index, name='index'),
]