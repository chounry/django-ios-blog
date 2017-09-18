from django.conf.urls import url
from . import views

app_name = 'home'

urlpatterns = [
    # /
    url(r'^$', views.home, name = 'home'),

    # /contact/
    url(r'^contact/', views.contact, name = 'contact'),

    # /personal/
    url(r'^personal/' , views.personal, name = 'personal'),


    # /blog/detail/<pk>/
    url(r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/(?P<day>[0-9]+)/(?P<slug>[-\w]+)/$', views.BlogDetail, name = 'blog-detail'),  # Change this

    # /blog/add-post
    url(r'add-post/$', views.CreatePost, name = 'add-post'),

    # /blog/slug/delete/
    url(r'^blog/(?P<slug>[-\w]+)/delete/$', views.delBlog, name = 'blog-delete'),

    # /blog/slug/update/
    url(r'^blog/(?P<slug>[-\w]+)/update/$', views.BlogUpdate, name = 'blog-update'),

    # search/q=sf
    url(r'^search/', views.search, name = 'search'),

    #/year/
    url(r'^(?P<year>[0-9]{4})/$', views.dateLookUp, name="year_lookup"),

    #/year/month/
    url(r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/$', views.dateLookUp, name="d-m_lookup"),

    #/year/month/day
    url(r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/(?P<day>[0-9]+)/$', views.dateLookUp, name="d-m-y_lookup"),
]