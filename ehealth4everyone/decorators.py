from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def practitioner_required(function=None, redirect_field_name=None, login_url='/accounts/login'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_practitioner,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def regular_user_required(function=None, redirect_field_name=None, login_url='/accounts/login'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and not u.is_practitioner,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator