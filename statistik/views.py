from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
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


def chart_view(request):
    context = {}

    chart = Chart.objects.get(pk=request.GET.get('id'))

    song_title = chart.song.title if len(
        chart.song.title) < 30 else chart.song.title[:30] + '...'
    title = ' // '.join([song_title, chart.get_type_display()])
    context['title'] = title
    if request.user.is_authenticated():
        if UserProfile.objects.get(
                user=request.user).max_reviewable >= chart.difficulty:
            if request.method == 'POST':
                form = ReviewForm(request.POST)
                if form.is_valid():
                    Review.objects.update_or_create(chart=chart,
                                                    user=request.user,
                                                    defaults=form.cleaned_data)
            else:
                matched_review = Review.objects.filter(
                    user=request.user).first()
                if matched_review:
                    data = {key: getattr(matched_review, key) for key in
                            ['text', 'clear_rating', 'hc_rating',
                             'exhc_rating', 'score_rating',
                             'characteristics']}
                    form = ReviewForm(data)
                else:
                    form = ReviewForm()
            context['form'] = form

    return render(request, 'chart.html', context)


def register_view(request):
    context = {}
    context['title'] = 'REGISTRATION'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data.get('username'),
                                            password=data.get('password'),
                                            email=data.get('email'))
            user.save()
            user_profile = UserProfile(user_id=user.id,
                                       dj_name=data.get('dj_name').upper(),
                                       location=data.get('location'),
                                       play_side=data.get('playside'),
                                       best_techniques=data.get('best_stats'),
                                       max_reviewable=0)
            user_profile.save()

            user = authenticate(username=data.get('username'),
                                password=data.get('password'))
            login(request, user)
            return redirect('ratings')
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
