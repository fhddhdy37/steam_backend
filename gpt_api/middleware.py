from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import get_token

class EnsureCsrfTokenMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == 'POST' and not request.META.get('CSRF_COOKIE'):
            get_token(request)
        return None