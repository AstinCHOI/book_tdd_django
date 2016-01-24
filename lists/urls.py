from django.conf.urls import url
from lists.views import view_list, new_list, my_lists, share_list


urlpatterns = [	
    # url(r'^lists/the-only-list-in-the-world/$', 'lists.views.view_list',
    #     name='view_list'
    # ),
    #url(r'^lists/(.+)/$', 'lists.views.view_list', name='view_list'),
    url(r'^(\d+)/$', view_list, name='view_list'),
    #url(r'^(\d+)/add_item$', views.add_item, name='add_item'),
    url(r'^new$', new_list, name='new_list'),
    # url(r'^new$', new_list2, name='new_list'),
    url(r'^users/(.+)/$', my_lists, name='my_lists'),
    url(r'^(\d+)/share$', share_list, name='share_list'),
]