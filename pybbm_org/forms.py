from account.forms import SignupForm
from captcha.fields import CaptchaField


class PybbmRegistrationForm(SignupForm):
    captcha = CaptchaField(label=u'I am human')