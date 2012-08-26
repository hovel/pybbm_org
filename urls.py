from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from forms import RegistrationFormCaptcha
from account.views import ChangePasswordView, SignupView, LoginView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^', include('pybb.urls', namespace='pybb')),
    url(r'^accounts/signup/$', SignupView.as_view(form_class=RegistrationFormCaptcha), name='registration_register'),
    (r'^accounts/', include('account.urls')),
    # aliases to match original django-registration urls
    url(r"^accounts/password/$", ChangePasswordView.as_view(), name="auth_password_change"),
    url(r"^accounts/login/$", LoginView.as_view(), name="auth_login"),

    (r'^captcha/', include('captcha.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)