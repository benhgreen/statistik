from django.http import HttpResponse
import datetime

from django.views.generic import TemplateView, View
from statistik.models import Chart


def index(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


class MiscView(TemplateView):
    template_name = 'misc.html'


class RatingsView(View):
    def get(self, request):
        query_params = {key: request.GET.get(key) for key in
                        ['type', 'difficulty'] if key in request.GET}
        print(query_params)
        matched_charts = Chart.objects.filter(**query_params)
        if request.GET.get('version'):
            matched_charts = [chart for chart in matched_charts if
                              chart.song.game_version == int(request.GET.get(
                                  'version'))]
        return HttpResponse('<br>'.join(
            ["%s[%s]" % (chart.song.title, chart.get_type_display()) for chart
             in matched_charts]))
