from django.contrib import admin
from django.urls import path, re_path
from photosite import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # path('', include('photosite.urls')),
    path('admin/', admin.site.urls),

    # path('api/login', views.login)

    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    re_path(r'^api/login/$', views.login),

    re_path(r'^api/messages/$', views.messages_list),
    re_path(r'^api/messages/add/$', views.add_message),
    re_path(r'^api/categories/$', views.categories_list),
    re_path(r'^api/categories/delete/(?P<pk>[0-9]+)$', views.delete_category),
    re_path(r'^api/categories/update/(?P<pk>[0-9]+)$', views.update_category),
    re_path(r'^api/categories/add/$', views.add_category),
]