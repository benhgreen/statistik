from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect
from django.views.generic import TemplateView
from statistik.constants import FULL_VERSION_NAMES, SORT_STYLES, \
    CHART_TYPE_CHOICES
from statistik.models import Chart


def index(request):
    return redirect('ratings')


class RatingsView(TemplateView):
    template_name = 'ratings.html'

    def get_context_data(self, **kwargs):
        context = super(RatingsView, self).get_context_data(**kwargs)
        filters = {}
        difficulty = self.request.GET.get('difficulty')
        version = self.request.GET.get('version')
        play_style = self.request.GET.get('style', 'SP')
        sort_style = SORT_STYLES.get(self.request.GET.get('sort'),
                                     'song__title')


        if version:
            filters['song__game_version'] = int(version)
        if difficulty:
            filters['difficulty'] = int(difficulty)
        if not (version or difficulty):
            difficulty = filters['difficulty'] = 12

        filters['type__in'] = {
            'SP': [0, 1, 2],
            'DP': [3, 4, 5]
        }[play_style]

        matched_charts = Chart.objects.filter(**filters).order_by(sort_style)
        context['charts'] = matched_charts

        title_elements = []
        if version:
            title_elements.append(FULL_VERSION_NAMES[int(version)].upper())
        if difficulty:
            title_elements.append('LV. ' + str(difficulty))
        title_elements.append(play_style)

        context['title'] = ' // '.join(title_elements)
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
