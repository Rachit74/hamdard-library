from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class AuthenticationRedirectMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Check if the response is a redirect to the login URL
        if response.status_code == 302 and response['Location'].startswith(settings.LOGIN_URL):
            from django.contrib import messages
            if request.path != settings.LOGIN_URL:
                # Add an error message if the user is redirected to the login page
                messages.error(request, 'You need to log in to access this page.')
        return response
