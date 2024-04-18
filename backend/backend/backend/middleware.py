from django.utils.deprecation import MiddlewareMixin

class LogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print(f"Request incoming on path: {request.path}")

    def process_response(self, request, response):
        print(f"Request to {request.path} responded with {response.status_code}")
        return response