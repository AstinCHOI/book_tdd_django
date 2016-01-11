from django.conf.urls import url
from django.contrib.auth.views import logout
from accounts.views import persona_login


urlpatterns = [
    url(r'^login$', persona_login, name='persona_login'),
    url(r'^logout$', logout, {'next_page': '/'}, name='logout'),
]


# spike mozilla persona
# urlpatterns = [
#     url(r'^login$', views.login, name='login'),
#     url(r'^logout$', views.logout, name='logout'),
# ]