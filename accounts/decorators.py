from django.http import HttpResponseForbidden
from functools import wraps

def traveler_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role != 'traveler':
            return HttpResponseForbidden("Access denied: Travelers only.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def provider_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role != 'provider':
            return HttpResponseForbidden("Access denied: Service Providers only.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
