from functools import wraps
from django.http import HttpResponseForbidden

def community_admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        community_id = kwargs.get('IDcommunity')
        user_roles = request.user.roles.filter(community_id=community_id, role='admin')
        if user_roles.exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("No tienes permisos de administrador para esta comunidad.")
    return _wrapped_view