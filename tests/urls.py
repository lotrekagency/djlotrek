from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns

def dummy_view(request):
    from django.http import HttpResponse
    return HttpResponse("Here's the text of the Web page.")

urlpatterns = [
    url(r'^sitemap\.xml$', dummy_view, name='sitemap'),
    url(r'^other$', dummy_view, name='other')
]

urlpatterns += i18n_patterns(
    url(r'^about$', dummy_view, name='about'),
    url(r'^news$', dummy_view, name='news'),
    prefix_default_language=False
)
