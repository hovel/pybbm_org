from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from forms import RegistrationFormCaptcha
from registration.views import register
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^', include('pybb.urls', namespace='pybb')),
    url(r'^accounts/register/$',
        register,
        kwargs={'form_class': RegistrationFormCaptcha},
        name='registration_register'),
    (r'^accounts/', include('registration.urls')),
    (r'^captcha/', include('captcha.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)