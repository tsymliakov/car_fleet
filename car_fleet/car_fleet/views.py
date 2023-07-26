from django.http import HttpResponse
from django.utils import timezone
from django.views import View
import datetime


class TimeView(View):
    def get(self, request, *args, **kwargs):

        # activate('Europe/Moscow')
        return HttpResponse(f'<p>Время UTC: {datetime.datetime.now()}</p>'
                            f'Время с часовым поясом: {timezone.localtime()}')
