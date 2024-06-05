from django.utils.deprecation import MiddlewareMixin
import json
from django.http import HttpResponseForbidden

class LogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        cookies = [cookie for cookie in request.COOKIES]
        print(f"Request incoming on path: {request.path} with cookies: {cookies}")

    def process_response(self, request, response):
        print(f"Request to {request.path} responded with {response.status_code}")
        return response

class LogSentCookiesMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        session_id = response.cookies.get('sessionid')
        csrf_token = response.cookies.get('csrftoken')

        if session_id:
            print(f"(MIDDLEWARE)Sent response with session ID: {session_id.value}")
        if csrf_token:
            print(f"(MIDDLEWARE)Sent response with CSRF token: {csrf_token.value}")

        return response

class InjectCsrfTokenMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        csrf_token = request.META.get('CSRF_COOKIE', None)
        if csrf_token and response.get('Content-Type') == 'application/json':
            try:
                response_data = json.loads(response.content)
                response_data['csrftoken'] = csrf_token
                response.content = json.dumps(response_data)
                response['Content-Type'] = 'application/json'
                response['Content-Length'] = len(response.content)
                print(f"(MIDDLEWARE) Injected CSRF token: {csrf_token}")
            except (json.JSONDecodeError, TypeError):
                pass
        return response
    


class PutCSRFTokenIntoHeader(MiddlewareMixin):
    def process_request(self, request):
        # Imprimir si el header CSRFToken ya está en la solicitud o no
        if 'HTTP_X_CSRFTOKEN' not in request.META:
            #print("HTTP_X_CSRFTOKEN no encontrado en los headers. Buscando en cookies...")
            csrf_token = request.COOKIES.get('csrftoken')
            if csrf_token:
                #print("CSRF token encontrado en cookies:", csrf_token)
                # Insertar el token CSRF en los headers de la solicitud
                request.META['HTTP_X_CSRFTOKEN'] = csrf_token
                #print("CSRF token insertado en los headers de la solicitud.")
            #else:
            #    print("CSRF token no encontrado en las cookies.")
        #else:
        #    print("HTTP_X_CSRFTOKEN ya está presente en los headers:", request.META['HTTP_X_CSRFTOKEN'])




class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.excluded_paths = [
            '/members/',
            '/members/register_user_community/',
            '/members/register/',
            '/members/login/',
            '/members/logout/',    
        ]

    def __call__(self, request):
        print(request.path)
        # Si la ruta solicitada está en la lista de excluidos, no aplicar la lógica del middleware
        if request.path in self.excluded_paths:
            return self.get_response(request)

        # Lógica del middleware antes de llamar a la vistañ
        response = self.get_response(request)
        # Lógica después de llamar a la vista
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path in self.excluded_paths:
            return None

        if not request.user.is_authenticated:
            return HttpResponseForbidden("No estás autenticado")

        community_id = view_kwargs.get('IDcommunity')
        if community_id:
            user_roles = request.user.roles.filter(community_id=community_id)
            if not user_roles.exists():
                return HttpResponseForbidden("No tienes permisos para acceder a esta comunidad")

        return None