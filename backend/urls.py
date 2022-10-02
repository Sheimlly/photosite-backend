from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from photosite import views
# from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),

    # Token
    re_path(r'^api/login/$', views.login),

    # Messages
    re_path(r'^api/messages/$', views.messages_list),
    re_path(r'^api/messages/(?P<pk>[0-9]+)$', views.message_details),
    re_path(r'^api/messages/add/$', views.add_message),

    # Categories
    re_path(r'^api/categories/$', views.categories_list),
    re_path(r'^api/categories/(?P<pk>[0-9]+)$', views.edit_category),

    # Offers
    re_path(r'^api/offers/$', views.offers_list),
    re_path(r'^api/offers/(?P<pk>[0-9]+)$', views.offer_details),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)