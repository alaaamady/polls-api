from django.http import JsonResponse


class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404 and not request.path.startswith('/static/'):
            return JsonResponse({'error': 'Page not found'}, status=404)
        return response
