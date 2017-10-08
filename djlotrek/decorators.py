from functools import wraps
from django.conf import settings

import requests


def check_recaptcha(view_func):
    """Chech that the entered recaptcha data is correct"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post(
                'https://www.google.com/recaptcha/api/siteverify',
                data=data
            )
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                error_message = 'Invalid reCAPTCHA. Please try again. '
                error_message += str(result['error-codes'])
                print(error_message)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
