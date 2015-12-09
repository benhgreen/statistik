import elo
import random

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from statistik.constants import (FULL_VERSION_NAMES, generate_version_urls,
                                 generate_level_urls)
from statistik.controller import (get_chart_data, generate_review_form,
                                  get_charts_by_ids, get_reviews_for_chart,
                                  get_reviews_for_user, get_user_list,
                                  create_new_user, elo_rate_charts)
from statistik.forms import RegisterForm


def index(request):
    return redirect('ratings')


class RatingsView(TemplateView):
    template_name = 'ratings.html'

    def get_context_data(self, **kwargs):
        context = super(RatingsView, self).get_context_data(**kwargs)
        difficulty = self.request.GET.get('difficulty')
        version = self.request.GET.get('version')
        play_style = self.request.GET.get('style', 'SP')
        user = self.request.user.id

        # assemble displayed info for each of the charts
        context['charts'] = get_chart_data(version, difficulty, play_style,
                                           user)

        # assemble page title
        # TODO uniform page title assembly which allows for links in title
        title_elements = []
        if version:
            title_elements.append(FULL_VERSION_NAMES[int(version)].upper())
        if difficulty:
            title_elements.append('LV. ' + str(difficulty))
        title_elements.append(play_style)
        context['title'] = ' // '.join(title_elements)
        context['page_title'] = 'STATISTIK // ' + context['title']

        # create version/level navigator to display above songlist
        context['versions'] = generate_version_urls()
        context['levels'] = generate_level_urls()

        return context


def chart_view(request):
    context = {}

    chart_id = request.GET.get('id')
    if not chart_id:
        return HttpResponseBadRequest()

    # TODO remove all direct interaction with chart
    chart = get_charts_by_ids([chart_id])[0]

   # truncate long song title
    song_title = chart.song.title if len(
        chart.song.title) < 30 else chart.song.title[:30] + '...'

    # assemble page title
    title = ' // '.join([song_title, chart.get_type_display()])
    context['title'] = title
    context['difficulty'] = chart.difficulty

    form_data = request.POST if request.method == 'POST' else None
    context['form'] = generate_review_form(request.user, chart_id,
                                           form_data)

    # get reviews for this chart, cache users for username and playside lookup
    context['reviews'] = get_reviews_for_chart(chart_id)

    # assemble page title
    context['page_title'] = 'STATISTIK // ' + context['title']
    return render(request, 'chart.html', context)


def elo_view(request):
    win = request.GET.get('win')
    lose = request.GET.get('lose')
    level = request.GET.get('level')

    is_hc = int(request.GET.get('hc', 0))
    # TODO extend to accommodate exhc and score types
    rate_type = 1 if is_hc else 0
    elo_type = 'elo_rating_hc' if is_hc else 'elo_rating'
    type_display = 'HC' if is_hc else 'NC'

    if not level:
        return HttpResponseBadRequest()

    # handle incoming elo reviews
    # TODO don't use GET for this
    if win and lose:
        draw = bool(request.GET.get('draw'))
        elo_rate_charts(int(win), int(lose), draw, elo_type)
        return HttpResponseRedirect(reverse('elo') + '?level=%s&hc=%s' %
                                    (level, rate_type))

    # handle regular requests
    else:
        display_list = bool(request.GET.get('list'))
        if display_list:
            # display list of charts ranked by elo
            # TODO fix line length
            matched_charts = Chart.objects.filter(difficulty=int(level),
                                                  type__lt=3)
            matched_charts.prefetch_related('song').order_by('-' + elo_type)

            # assemble displayed elo info for matched charts
            # TODO add link to 'normal' chart reviews
            context = {
                'chart_list': [{
                                  'index': ind + 1,
                                  'id': chart.id,
                                  'title': chart.song.title,
                                  'type': chart.get_type_display(),
                                  'rating': round(getattr(chart, elo_type), 3)
                               } for ind, chart in enumerate(matched_charts)],
                'title': ' // '.join(
                    ['ELO', level + '☆', type_display + ' LIST'])
            }
        else:
            # display two songs to rank
            elo_diff = 9001
            chart1 = chart2 = None
            charts = list(Chart.objects.filter(difficulty=int(level),
                                               type__lt=3))

            # only return closely-matched charts for better rankings
            while elo_diff > 50:
                [chart1, chart2] = random.sample(charts, 2)
                elo_diff = abs(chart1.elo_rating-chart2.elo_rating)

            # assemble display info for these two charts
            context = {title: {
                'title': chart.song.title,
                'type': chart.get_type_display(),
                'id': chart.id
            } for [title, chart] in [['chart1', chart1], ['chart2', chart2]]}

            # add page title
            context['title'] = ' // '.join(
                ['ELO', level+'☆', type_display + ' RATE'])

    context['page_title'] = 'STATISTIK // ' + context['title']
    context['level'] = level
    context['is_hc'] = rating_type
    context['is_hc_display'] = type_display
    return render(request, 'elo_rating.html', context)


def user_view(request):
    context = {}
    user_id = request.GET.get('id')
    if user_id:
        # make sure this user actually exists
        user = User.objects.filter(pk=user_id).first()
        if not user:
            return HttpResponseBadRequest()

        context['review'] = get_reviews_for_user(user.id)

        # assemble page title
        context['title'] = ' // '.join([user.username.upper(), 'REVIEWS'])
        context['page_title'] = 'STATISTIK // ' + context['title']

        return render(request, 'user.html', context)

    else:
        # return list of all registered users
        context['users'] = get_user_list()

        # assemble page title
        context['title'] = 'USERS'
        context['page_title'] = 'STATISTIK // ' + context['title']

        return render(request, 'userlist.html', context)


def register_view(request):
    context = {}
    if request.method == 'POST':
        # handle submitted registrations
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # TODO verify user was actually created
            create_new_user(data)
            user = authenticate(username=data.get('username'),
                                password=data.get('password'))
            login(request, user)
            return redirect('ratings')
    else:
        # display blank form
        form = RegisterForm()
    context['form'] = form

    # assemble page title
    context['title'] = 'REGISTRATION'
    context['page_title'] = 'STATISTIK // ' + context['title']

    return render(request, 'register.html', context)


def login_view(request):
    # TODO make this a proper form to display errors and stuff
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
