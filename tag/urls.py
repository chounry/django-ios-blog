from django.conf.urls import url

from . import views

app_name = 'tag'

urlpatterns = [
    url(r'^(?P<tag>[-&\w]+)/', views.tagView, name = 'filter-tag' )
]