from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from statistik.constants import FULL_VERSION_NAMES, \
    generate_version_urls, generate_level_urls
from statistik.forms import ReviewForm, RegisterForm
from statistik.models import Chart, Review, UserProfile


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

        matched_charts = Chart.objects.filter(**filters).prefetch_related(
            'song').order_by('song__game_version')
        context['charts'] = [{
                                 'id': chart.id,
                                 'title': chart.song.title,
                                 'alt_title': chart.song.alt_title if chart.song.alt_title else chart.song.title,
                                 'note_count': chart.note_count,
                                 'difficulty': chart.difficulty,
                                 'avg_clear_rating': chart.avg_clear_rating,
                                 'avg_hc_rating': chart.avg_hc_rating,
                                 'avg_exhc_rating': chart.avg_exhc_rating,
                                 'avg_score_rating': chart.avg_score_rating,
                                 'game_version': chart.song.game_version,
                                 'game_version_display': chart.song.get_game_version_display(),
                                 'type_display': chart.get_type_display()
                             } for chart in matched_charts]

        title_elements = []
        if version:
            title_elements.append(FULL_VERSION_NAMES[int(version)].upper())
        if difficulty:
            title_elements.append('LV. ' + str(difficulty))
        title_elements.append(play_style)
        context['title'] = ' // '.join(title_elements)

        context['versions'] = generate_version_urls()
        context['levels'] = generate_level_urls()

        return context


class ChartView(TemplateView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super(ChartView, self).get_context_data(**kwargs)
        chart = Chart.objects.get(pk=self.request.GET.get('id'))

        song_title = chart.song.title if len(
            chart.song.title) < 30 else chart.song.title[:20] + '...'
        title = ' // '.join([song_title, chart.get_type_display()])
        context['title'] = title
        if self.request.user.is_authenticated():
            if UserProfile.objects.get(
                    user=self.request.user).max_reviewable >= chart.difficulty:
                context['title'] = 'yey'
                if self.request.method == 'POST':
                    form = ReviewForm(self.request.POST)
                    if form.is_valid():
                        pass
                else:
                    form = ReviewForm()
                    matched_review = Review.filter(user=self.request.user)

        return context

def register_view(request):
    context = {}
    context['title'] = 'STATISTIK // REGISTRATION'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        context['title'] = 'shit'
    else:
        form = RegisterForm()
    context['form'] = form
    return render(request, 'register.html', context)


def login_view(request):
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