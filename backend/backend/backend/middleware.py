from django.utils.deprecation import MiddlewareMixin

class LogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        cookies = [cookie for cookie in request.COOKIES]
        #print(f"Request incoming on path: {request.path} with cookies: {cookies}")

    def process_response(self, request, response):
        #print(f"Request to {request.path} responded with {response.status_code}")
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