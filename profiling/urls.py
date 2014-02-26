from django.conf.urls import patterns, include, url
from app import views
from django.contrib import admin

# admin.autodiscover()

urlpatterns = patterns('',

    # url(r'^admin/', include(admin.site.urls)),
    #url(r'start/', 'app.views.index'),
    url(r'^prof/$', views.UserListView.as_view()),

)
