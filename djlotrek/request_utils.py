
def get_host_url(request):
    if request:
        return '{0}://{1}'.format(
            request.scheme, request.META['HTTP_HOST']
        )
