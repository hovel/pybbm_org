from registration.forms import RegistrationFormUniqueEmail
from captcha.fields import CaptchaField

class RegistrationFormCaptcha(RegistrationFormUniqueEmail):

    captcha = CaptchaField(label=u'I am human')