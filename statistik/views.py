"""
Main view controller for Statistik
"""
import json

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import (HttpResponseBadRequest, HttpResponseRedirect,
                         HttpResponse)
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _
from statistik.constants import (FULL_VERSION_NAMES, generate_version_urls,
                                 generate_level_urls, SCORE_CATEGORY_CHOICES,
                                 generate_elo_level_urls, IIDX, DDR, GAMES, GAME_CHOICES)
from statistik.controller import (get_chart_data, generate_review_form,
                                  get_charts_by_ids, get_reviews_for_chart,
                                  get_reviews_for_user, get_user_list,
                                  create_new_user, elo_rate_charts,
                                  get_elo_rankings, make_elo_matchup,
                                  create_page_title, make_nav_links,
                                  generate_user_form, delete_review, make_game_links)
from statistik.forms import RegisterForm, DDRSearchForm, IIDXSearchForm


def index(request, game='IIDX'):
    """
    Returns index page
    :param request: Request to handle
    :param game:    The game to show the page for (from GAME_CHOICES)
    :rtype HTTPResponse:
    """
    reverse_kwargs = {'game': game}
    context = {
        'index_links': [
            (_('STANDARD RATINGS'), reverse('ratings', kwargs=reverse_kwargs)),
            (_('ELO RATINGS'), reverse('elo', kwargs=reverse_kwargs)),
            (_('USER LIST'), reverse('users')),
            (_('SEARCH'), reverse('search', kwargs=reverse_kwargs))
        ],

        'title': 'STATISTIK // ' + _('INDEX') + ' // ' + game,
        'page_title': 'STATISTIK // ' + _('INDEX') + ' // ' + game,
        'game_links': make_game_links(GAMES[game])
    }
    return render(request, 'index.html', context)


def ratings_view(request, game='IIDX'):
    """
    Assemble ratings page. Possible filters include difficulty and version.
    :param request: Request to handle
    :param game:    The game to show the page for (from GAME_CHOICES)
    :rtype dict: Context including chart data
    """
    # game = int(request.GET.get('game', IIDX))
    difficulty = request.GET.get('difficulty')
    versions = request.GET.getlist('version')
    play_style = request.GET.get('style', 'SP')
    user = request.user.id

    # if versions:
    #     game = int(versions[0]) // 100

    # remove any None keys to avoid having to check for them later
    params = {k: v for k, v in {
        'min_difficulty': request.GET.get('min_difficulty'),
        'max_difficulty': request.GET.get('max_difficulty'),
        'title': request.GET.get('title'),
        'genre': request.GET.get('genre'),
        'artist': request.GET.get('artist'),
        'play_style': request.GET.get('play_style'),
        'min_nc': request.GET.get('min_nc'),
        'max_nc': request.GET.get('max_nc'),
        'min_hc': request.GET.get('min_hc'),
        'max_hc': request.GET.get('max_hc'),
        'min_exhc': request.GET.get('min_exhc'),
        'max_exhc': request.GET.get('max_exhc'),
        'min_score': request.GET.get('min_score'),
        'max_score': request.GET.get('max_score'),
        'techs': request.GET.getlist('techs')
    }.items() if v}

    # if not a search and nothing was specified, show 12a
    if not request.GET.get('submit') and not (difficulty or versions):
        difficulty = 12

    chart_data = get_chart_data(GAMES[game], versions, difficulty, play_style, user, params,
                                include_reviews=bool(request.GET.get('json')))

    if request.GET.get('json'):
        return HttpResponse(
            json.dumps({'data': chart_data}, indent=4, ensure_ascii=False))

    _generate_chart_difficulty_display(chart_data)
    _generate_chart_bpm_display(chart_data)

    # assemble displayed info for each of the charts
    context = {
        'charts': chart_data
    }

    # assemble page title
    title_elements = []
    if request.GET.get('submit'):
        title_elements.append('SEARCH RESULTS')
    else:
        # title_elements.insert(0, {0: 'IIDX', 1: 'DDR'}[game])
        title_elements.insert(0, game)
        if versions:
            title_elements.append(FULL_VERSION_NAMES[GAMES[game]][int(versions[0])].upper())
        if difficulty or not (difficulty or versions[0]):
            title_elements.append('LV. ' + str(difficulty or 12))
        title_elements.append(play_style)
    create_page_title(context, title_elements)

    # create version/level navigator to display above songlist
    context['versions'] = generate_version_urls(GAMES[game])
    context['levels'] = generate_level_urls(GAMES[game])

    context['nav_links'] = make_nav_links(game=GAMES[game])

    if game == 'IIDX':
        return render(request, 'ratings_iidx.html', context)
    else:
        return render(request, 'ratings_ddr.html', context)


def chart_view(request, chart_id=None):
    """
    Handle requests for individual chart pages (mostly collections of reviews)
    :param chart_id: The id of the chart to show
    :param request: Request to handle
    """
    context = {}

    # chart_id = request.GET.get('id')
    if not chart_id:
        return HttpResponseBadRequest()
    chart_id = int(chart_id)

    if request.GET.get('delete') == 'true' and request.user.is_authenticated():
        delete_review(request.user.id, chart_id)
        return HttpResponseRedirect(reverse('chart', kwargs={'chart_id': chart_id}))

    # TODO remove all direct interaction with chart
    chart = get_charts_by_ids([chart_id])[0]

    # truncate long song title
    song_title = chart.song.title if len(
            chart.song.title) <= 15 else chart.song.title[:15] + '...'

    # assemble page title
    title_elements = [song_title,
                      chart.get_type_display(),
                      str(chart.difficulty) + '☆']
    create_page_title(context, title_elements)

    context['difficulty'] = chart.difficulty
    context['chart_id'] = chart_id

    form_data = request.POST if request.method == 'POST' else None
    context['form'], context['review_exists'] = generate_review_form(
            request.user, chart_id, form_data)

    # get reviews for this chart, cache users for username and playside lookup
    context['reviews'] = get_reviews_for_chart(chart_id)
    if chart.song.game == IIDX:
        style = chart.get_type_display()[:2]
    else:
        style = chart.get_type_display()[1:]
        # if difficulty is beginner, make it SP
        if style[0] == 'E':
            style = 'SP'

    context['nav_links'] = make_nav_links(game=chart.song.game,
                                          level=chart.difficulty,
                                          style=style,
                                          version=chart.song.game_version)
    if chart.song.game == IIDX:
        return render(request, 'chart_iidx.html', context)
    else:
        return render(request, 'chart_ddr.html', context)


def elo_view(request, game='IIDX'):
    """
    Handle requests for Elo views (lists as well as individual matchups)
    :param request: Request to handle
    """

    win = request.GET.get('win')
    lose = request.GET.get('lose')
    level = request.GET.get('level', '12')
    display_list = bool(request.GET.get('list'))
    clear_type = int(request.GET.get('type', 0))
    # game = int(request.GET.get('game', IIDX))

    if not (display_list or request.user.is_authenticated()):
        return HttpResponseRedirect(
                reverse('elo', kwargs={'game': game}) + '?level=%s&type=%d&list=true' %
                (level, clear_type))

    # TODO extend to accommodate exhc and score types
    rate_type_column = 'elo_rating_hc' if clear_type == 1 else 'elo_rating'
    type_display = SCORE_CATEGORY_CHOICES[GAMES[game]][clear_type][1]

    # handle incoming elo reviews
    # TODO don't use GET for this
    if win and lose:
        draw = bool(request.GET.get('draw'))
        elo_rate_charts(int(win), int(lose), request.user, draw, clear_type)
        return HttpResponseRedirect(reverse('elo', kwargs={'game': game}) + '?level=%s&type=%d' %
                                    (level, clear_type))

    # handle regular requests
    else:
        context = {}
        if display_list:
            # display list of charts ranked by elo
            # TODO fix line length
            context['chart_list'] = get_elo_rankings(GAMES[game], level, rate_type_column)
            title_elements = ['ELO', game + ' ' + level + '☆ ' + type_display + _(' LIST')]
        else:
            # display two songs to rank
            [context['chart1'], context['chart2']] = make_elo_matchup(GAMES[game], level)

            # add page title
            title_elements = ['ELO', game + ' ' + level + '☆ ' + type_display + _(' MATCHING')]

    create_page_title(context, title_elements)
    context['game'] = game
    context['level'] = level
    context['is_hc'] = clear_type
    context['is_hc_display'] = type_display
    context['level_links'] = generate_elo_level_urls(GAMES[game])
    context['nav_links'] = make_nav_links(
            level=int(level),
            elo='list' if display_list else 'match',
            clear_type=clear_type,
            game=GAMES[game])
    return render(request, 'elo_rating.html', context)


def user_view(request, user_id=None):
    """
    Handle requests for both individual user pages as well as the userlist
    :param request: Request to handle
    :param user_id: The ID of the user to show, or None to show a list of all users
    """
    context = {}
    if user_id:
        # make sure this user actually exists
        user = User.objects.filter(pk=user_id).first()
        if not user:
            return HttpResponseBadRequest()

        user_reviews = get_reviews_for_user(user.id)
        if IIDX in user_reviews:
            context['iidx_reviews'] = user_reviews[IIDX]
        if DDR in user_reviews:
            context['ddr_reviews'] = user_reviews[DDR]

        # if user is the logged in user, let them edit their options
        if request.user.id == int(user_id):
            context['form'] = generate_user_form(request.user, request.POST)

        # assemble page title
        title_elements = [user.username.upper(), _('REVIEWS')]
        create_page_title(context, title_elements)

        context['nav_links'] = make_nav_links(user=True)

        return render(request, 'user.html', context)

    else:
        # return list of all registered users
        context['users'] = get_user_list()

        # assemble page title
        title_elements = [_('USER LIST')]
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
            try:
                create_new_user(data)
            except IntegrityError:
                form.add_error('username', 'Username taken.')
            else:
                user = authenticate(username=data.get('username'),
                                    password=data.get('password'))
                login(request, user)
                return redirect('index')
    else:
        # display blank form
        form = RegisterForm()
    context['form'] = form

    # assemble page title
    title_elements = [_('REGISTRATION')]
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

    return redirect('index')


def logout_view(request):
    """
    Logs out current user and redirects to index page
    :param request: Request to handle
    """
    logout(request)
    return redirect('index')


def search_view(request, game='IIDX'):


    """
    GET only, gives the user a search form
    :param request: Request to handle
    :param game: The game to search charts from
    """
    context = {}
    title_elements = ['SEARCH']
    create_page_title(context, title_elements)
    if 'submit' in request.GET:
        if game == 'DDR':
            form = DDRSearchForm(request.GET)
        else:
            form = IIDXSearchForm(request.GET)
        if form.is_valid():
            # pass on the search filters to the ratings view
            response = redirect(reverse('ratings', kwargs={'game': game}))
            # delete any filters left empty or at the default to clean up the URL
            query = request.GET.copy()
            empty = []
            # can't delete while iterating over the query so mark them
            for key in query:
                if key != 'submit':
                    if not query[key] or query[key] == str(form.fields[key].initial):
                        empty.append(key)
            for key in empty:
                del (query[key])
            response['Location'] += '?' + query.urlencode()
            return response
    else:
        if game == 'DDR':
            form = DDRSearchForm()
        else:
            form = IIDXSearchForm()
    context['form'] = form
    context['nav_links'] = make_nav_links(game=GAMES[game])
    context['game'] = game
    return render(request, 'search.html', context)

# TODO: These don't really belong here...move them somewhere else
def _generate_chart_difficulty_display(chart_data):
    for chart in chart_data:
        if 'has_reviewed' in chart:
            if chart['has_reviewed']:
                chart['difficulty'] = str(chart['difficulty']) + "★"
            else:
                chart['difficulty'] = str(chart['difficulty']) + "☆"
        else:
            chart['difficulty'] = str(chart['difficulty'])

    return chart_data

def _generate_chart_bpm_display(chart_data):
    for chart in chart_data:
        if 'bpm_min' in chart:
            if 'bpm_max' in chart and chart['bpm_min'] != chart['bpm_max']:
                chart['bpm'] = "{0} - {1}".format(chart['bpm_min'], chart['bpm_max'])
            else:
                chart['bpm'] = str(chart['bpm_min']) 
        else:
            chart['bpm'] = '--'
    
    return chart_data