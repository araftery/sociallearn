import profiles.models, django.utils.timezone

class StreaksMiddleware(object):
    def process_request(self, request):
        if request.user:
            profiles.models.Visit(time=django.utils.timezone.now(), student=request.user.student).save()
