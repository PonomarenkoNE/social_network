from django.utils import timezone

from .models import User


class UpdateLastRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Update user's last_request time if user is authenticated
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.pk)
            user.last_request = timezone.now()
            user.save()

        return response
