from account.views import SignupView
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import TemplateView
from pybbm_org.forms import PybbmRegistrationForm

admin.autodiscover()

urlpatterns = [
    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('pybb.urls', namespace='pybb')),
    url(r'^accounts/signup/$', SignupView.as_view(form_class=PybbmRegistrationForm), name='registration_register'),

    url(r"^accounts/", include("account.urls")),
    url(r'^captcha/', include('captcha.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
