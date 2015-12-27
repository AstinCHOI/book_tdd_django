from django.conf.urls import include, url
from . import views

urlpatterns = [	
    # url(r'^lists/the-only-list-in-the-world/$', 'lists.views.view_list',
    #     name='view_list'
    # ),
    #url(r'^lists/(.+)/$', 'lists.views.view_list', name='view_list'),
    url(r'^(\d+)/$', views.view_list, name='view_list'),
    url(r'^(\d+)/add_item$', views.add_item, name='add_item'),
    url(r'^new$', views.new_list, name='new_list'),
]