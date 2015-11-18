from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
import datetime

from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from statistik.models import Chart


def index(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


class MiscView(TemplateView):
    template_name = 'misc.html'


class RatingsView(TemplateView):
    template_name = 'ratings.html'

    def get_context_data(self, **kwargs):
        context = super(RatingsView, self).get_context_data(**kwargs)
        difficulty = self.request.GET.get('difficulty') or 12
        context['charts'] = Chart.objects.filter(difficulty=difficulty,
                                                 type__in=[0, 1, 2]).extra(order_by='')
        context['difficulty'] = difficulty
        return context


def login_view(request):
    print(request.POST)
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)

    return redirect('ratings')


def logout_view(request):
    logout(request)
    return redirect('ratings')