from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^', include('pybb.urls', namespace='pybb')),
    (r'^accounts/', include('registration.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)