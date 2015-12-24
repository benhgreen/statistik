"""
Main view controller for Statistik
"""

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from statistik.constants import (FULL_VERSION_NAMES, generate_version_urls,
                                 generate_level_urls, SCORE_CATEGORY_CHOICES)
from statistik.controller import (get_chart_data, generate_review_form,
                                  get_charts_by_ids, get_reviews_for_chart,
                                  get_reviews_for_user, get_user_list,
                                  create_new_user, elo_rate_charts,
                                  get_elo_rankings, make_elo_matchup,
                                  create_page_title, make_nav_links)
from statistik.forms import RegisterForm


def index(request):
    """
    Returns index page
    :param request: Request to handle
    :rtype HTTPResponse:
    """
    context = {
        'index_links': [
            ('STANDARD RATINGS', reverse('ratings')),
            ('ELO RATINGS', reverse('elo')),
            ('USER LIST', reverse('users'))
        ],

        'title': 'STATISTIK // INDEX',
        'page_title': 'STATISTIK // INDEX'
    }
    return render(request, 'index.html', context)


class RatingsView(TemplateView):
    """
    Handles requests for rating chart pages
    """
    template_name = 'ratings.html'

    def get_context_data(self):
        """
        Assemble ratings page. Possible filters include difficulty and version.
        :rtype dict: Context including chart data
        """
        context = super(RatingsView, self).get_context_data()
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
        if difficulty or not (difficulty or version):
            title_elements.append('LV. ' + str(difficulty or 12))
        title_elements.append(play_style)
        create_page_title(context, title_elements)

        # create version/level navigator to display above songlist
        context['versions'] = generate_version_urls()
        context['levels'] = generate_level_urls()

        return context


def chart_view(request):
    """
    Handle requests for individual chart pages (mostly collections of reviews)
    :param request: Request to handle
    """
    context = {}

    chart_id = request.GET.get('id')
    if not chart_id:
        return HttpResponseBadRequest()

    # TODO remove all direct interaction with chart
    chart = get_charts_by_ids([chart_id])[0]

    # truncate long song title
    song_title = chart.song.title if len(
        chart.song.title) < 15 else chart.song.title[:15] + '...'

    # assemble page title
    title_elements = [song_title,
                      chart.get_type_display(),
                      str(chart.difficulty) + '☆']
    create_page_title(context, title_elements)


    context['difficulty'] = chart.difficulty

    form_data = request.POST if request.method == 'POST' else None
    context['form'] = generate_review_form(request.user, chart_id,
                                           form_data)

    # get reviews for this chart, cache users for username and playside lookup
    context['reviews'] = get_reviews_for_chart(chart_id)

    context['nav_links'] = make_nav_links(level=chart.difficulty,
                                          style=chart.get_type_display()[:2],
                                          version=chart.song.game_version)

    return render(request, 'chart.html', context)


def elo_view(request):
    """
    Handle requests for Elo views (lists as well as individual matchups)
    :param request: Request to handle
    """
    win = request.GET.get('win')
    lose = request.GET.get('lose')
    level = request.GET.get('level')

    clear_type = int(request.GET.get('type', 0))
    # TODO extend to accommodate exhc and score types
    rate_type_column = 'elo_rating_hc' if clear_type == 1 else 'elo_rating'
    type_display = SCORE_CATEGORY_CHOICES[clear_type][1]

    if not level:
        return HttpResponseBadRequest()

    # handle incoming elo reviews
    # TODO don't use GET for this
    if win and lose:
        draw = bool(request.GET.get('draw'))
        elo_rate_charts(int(win), int(lose), draw, clear_type)
        return HttpResponseRedirect(reverse('elo') + '?level=%s&type=%d' %
                                    (level, clear_type))

    # handle regular requests
    else:
        context = {}
        display_list = bool(request.GET.get('list'))
        if display_list:
            # display list of charts ranked by elo
            # TODO fix line length
            context['chart_list'] = get_elo_rankings(level, rate_type_column)
            title_elements = ['ELO ' + level + '☆', type_display + ' LIST']
        else:
            # display two songs to rank
            [context['chart1'], context['chart2']] = make_elo_matchup(level)

            # add page title
            title_elements = ['ELO ' + level + '☆', type_display + ' MATCHING']

    create_page_title(context, title_elements)
    context['level'] = level
    context['is_hc'] = clear_type
    context['is_hc_display'] = type_display
    context['nav_links'] = make_nav_links(
            level=int(level),
            elo='list' if display_list else 'match',
            clear_type=clear_type)
    return render(request, 'elo_rating.html', context)


def user_view(request):
    """
    Handle requests for both individual user pages as well as the userlist
    :param request: Request to handle
    """
    context = {}
    user_id = request.GET.get('id')
    if user_id:
        # make sure this user actually exists
        user = User.objects.filter(pk=user_id).first()
        if not user:
            return HttpResponseBadRequest()

        context['review'] = get_reviews_for_user(user.id)

        # assemble page title
        title_elements = [user.username.upper(), 'REVIEWS']
        create_page_title(context, title_elements)

        context['nav_links'] = make_nav_links(user=True)

        return render(request, 'user.html', context)

    else:
        # return list of all registered users
        context['users'] = get_user_list()

        # assemble page title
        title_elements =  ['USER LIST']
        create_page_title(context, title_elements)
        context['nav_links'] = make_nav_links()

        return render(request, 'userlist.html', context)


def register_view(request):
    """
    Handle user registration
    :param request: Request to handle
    """
    context = {}
    if request.method == 'POST':
        # handle submitted registration forms
        # TODO refactor RegisterForm creation to somewhere else
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
    title_elements =  ['REGISTRATION']
    create_page_title(context, title_elements)

    return render(request, 'register.html', context)


def login_view(request):
    """
    POST only, handles user login
    :param request: Request to handle
    """
    # TODO make this a proper form to display errors and stuff
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)

    return redirect('ratings')


def logout_view(request):
    """
    Logs out current user and redirects to index page
    :param request: Request to handle
    """
    logout(request)
    return redirect('ratings')
