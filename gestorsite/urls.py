
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from django.views.generic import TemplateView


urlpatterns = [

    path('', include('a_Account.urls')),
    path('', include('a_Acl.urls')),
    path('', include('a_Content.urls')),
    path('', include('a_Site.urls.manage_url')),
    path('admin/', admin.site.urls),
    path('', include('a_Site.urls.portal_url'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
    # import debug_toolbar
    # urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
    # urlpatterns = [
    #     re_path(r'^__debug__/', include(debug_toolbar.urls))
    # ] + urlpatterns