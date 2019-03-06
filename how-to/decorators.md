# Our @decorators

## Google reCaptcha v2 (server auth) 
Use `@check_recaptcha` on your POST handler_function


- `settings.py`
```py
GOOGLE_RECAPTCHA_SECRET_KEY = 'your-server-key'
```

- `views.py`
```py
from djlotrek.decorators import check_recaptcha


@check_recaptcha
def my_view(request):
    if request.recaptcha_is_valid:
        print('Recaptcha is valid, go on')
    else:
        print("you are a robot, and we don't like robot")
```
- `your-template.html`
```html
<form method="POST">
    <script src='https://www.google.com/recaptcha/api.js'></script>
    <div class="g-recaptcha" data-sitekey="your-client-key"></div>
</form>

```
### How to generate both key | reCAPTCHA v2  - I'm not a robot - Checkbox
[https://www.google.com/recaptcha/admin/create](https://www.google.com/recaptcha/admin/create)

If you use it on localhost, set `127.0.0.1` on domains of keys


---
[Turn back](/README.md)
