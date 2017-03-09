from django.conf import settings as django_settings

def settings(request):
    # dict_settings = dict()
    # for key in django_settings._explicit_settings:
    #     dict_settings[key] = getattr(settings,key)
    return {'settings': django_settings}
