import time

from django.utils.deprecation import MiddlewareMixin


class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        end_time = time.time()
        duration = end_time - request.start_time
        print(f"API: {request.path}, Params: {request.GET}, Duration: {duration:.2f}s")
        return response
