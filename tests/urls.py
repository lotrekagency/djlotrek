from django.conf.urls import url, include

def dummy_view(request):
    from django.http import HttpResponse
    return HttpResponse("Here's the text of the Web page.")

urlpatterns = [
    url(r'^sitemap\.xml$', dummy_view, name='sitemap'),
    url(r'^other$', dummy_view, name='other')
]
