from django.utils.deprecation import MiddlewareMixin

class LogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        cookies = [cookie for cookie in request.COOKIES]
        print(f"Request incoming on path: {request.path} with cookies: {cookies}")

    def process_response(self, request, response):
        print(f"Request to {request.path} responded with {response.status_code}")
        return response
