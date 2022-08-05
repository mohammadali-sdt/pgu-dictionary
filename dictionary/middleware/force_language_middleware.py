from django.conf import settings
from django.utils import translation


def force_lang_middleware(get_response):
    def middleware(request):
        language_header = 'HTTP_ACCEPT_LANGUAGE'
        if language_header in request.META:
            del request.META[language_header]

        response = get_response(request)
        return response

    return middleware
