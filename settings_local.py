__author__ = 'zeus'


def check_superuser(user, post):
    if user.is_superuser:
        return True
    return False

PYBB_PREMODERATION = check_superuser

PYBB_ENABLE_ANONYMOUS_POST = True