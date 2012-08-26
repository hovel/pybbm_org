from account.forms import SignupForm
from captcha.fields import CaptchaField

class RegistrationFormCaptcha(SignupForm):

    captcha = CaptchaField(label=u'I am human')