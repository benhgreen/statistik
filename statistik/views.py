import random
import statistics

import elo

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from statistik.constants import (FULL_VERSION_NAMES,
    generate_version_urls, generate_level_urls, TECHNIQUE_CHOICES,
    RECOMMENDED_OPTIONS_CHOICES, SCORE_CATEGORY_NAMES)
from statistik.forms import ReviewForm, RegisterForm
from statistik.models import Chart, Review, UserProfile, EloReview


def index(request):
    return redirect('ratings')


def organize_reviews(matched_reviews, user_id):
    """
    Helper method for get_avg_ratings.
    :param Queryset matched_reviews: Queryset(or iterable) of Review objects
    :param int user_id: User id to identify which charts that user has rated
    :rtype tuple: Tuple containing a dict mapping chart ids to lists of their
                  reviews, as well as a set of the ids of charts that have
                  been reviewed by this user
    """
    review_dict = {}
    user_reviewed = set([review.chart_id for review in matched_reviews
                         if review.user_id == user_id])
    for review in matched_reviews:
        if review.chart_id in review_dict:
            review_dict[review.chart_id].append(review)
        else:
            review_dict[review.chart_id] = [review]
    return review_dict, user_reviewed


def get_avg_ratings(chart_ids, user_id=None):
    """
    Get average ratings for all charts.
    :param list chart_ids: List of chart ids to retrieve ratings for
    :param int user_id: User id to identify which charts that user has rated
    :rtype dict:  Dict mapping chart ids to a dict of the average ratings for
                  that chart as well as a has_reviewed boolean.
    """
    matched_reviews = Review.objects.filter(chart__in=chart_ids)
    organized_reviews, reviewed_charts = organize_reviews(matched_reviews,
                                                          user_id=user_id)
    ret = {}

    for chart in chart_ids:
        ret[chart] = {}
        # get reviews for this chart
        specific_reviews = organized_reviews.get(chart)
        if specific_reviews:
            # for each rating type, average the scores in matched reviews
            for rating_type in SCORE_CATEGORY_NAMES:
                avg_rating = "%.1f" % round(statistics.mean(
                    [getattr(review, rating_type)
                     for review in specific_reviews
                     if getattr(review, rating_type) is not None] or [0]), 1)

                # if average is '0.0', normalize that to 0
                if avg_rating != "0.0":
                    ret[chart][rating_type] = avg_rating
                else:
                    ret[chart][rating_type] = 0

            # set 'has_reviewed' if the user has reviewed this chart
            ret[chart]['has_reviewed'] = (chart in reviewed_charts)

        # winding up here means no reviews were found for one of the charts
        # which means the template will just use '--' for all the ratings
        else:
            ret[chart] = {}

    return ret


class RatingsView(TemplateView):
    template_name = 'ratings.html'

    def get_context_data(self, **kwargs):
        context = super(RatingsView, self).get_context_data(**kwargs)
        filters = {}
        difficulty = self.request.GET.get('difficulty')
        version = self.request.GET.get('version')
        play_style = self.request.GET.get('style', 'SP')

        # create filters for songlist based off GET params
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

        matched_chart_ids = [chart.id for chart in matched_charts]

        # get avg ratings for the charts in the returned queryset
        avg_ratings = get_avg_ratings(matched_chart_ids, self.request.user.id)

        # assemble displayed info for each of the charts
        # TODO fix line length
        context['charts'] = [{
                                 'id': chart.id,
                                 'title': chart.song.title,
                                 'alt_title': chart.song.alt_title if chart.song.alt_title else chart.song.title,
                                 'note_count': chart.note_count,
                                 'difficulty': chart.difficulty,
                                 'avg_clear_rating': avg_ratings[chart.id].get(
                                     'clear_rating'),
                                 'avg_hc_rating': avg_ratings[chart.id].get(
                                     'hc_rating'),
                                 'avg_exhc_rating': avg_ratings[chart.id].get(
                                     'exhc_rating'),
                                 'avg_score_rating': avg_ratings[chart.id].get(
                                     'score_rating'),
                                 'game_version': chart.song.game_version,
                                 'game_version_display': chart.song.get_game_version_display(),
                                 'type_display': chart.get_type_display(),
                                 'has_reviewed': avg_ratings[chart.id].get(
                                     'has_reviewed'
                                 )
                             } for chart in matched_charts]

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

    chart = Chart.objects.get(pk=request.GET.get('id'))

    # truncate long song title
    song_title = chart.song.title if len(
        chart.song.title) < 30 else chart.song.title[:30] + '...'

    # assemble page title
    title = ' // '.join([song_title, chart.get_type_display()])
    context['title'] = title
    context['difficulty'] = chart.difficulty

    # if user is authenticated and can review this chart, display review form
    if request.user.is_authenticated():
        if UserProfile.objects.get(
                user=request.user).max_reviewable >= chart.difficulty:

            # handle incoming reviews
            if request.method == 'POST':
                form = ReviewForm(request.POST)
                if form.is_valid(difficulty=chart.difficulty):
                    Review.objects.update_or_create(chart=chart,
                                                    user=request.user,
                                                    defaults=form.cleaned_data)
            # handle regular page requests
            else:
                # check if user has an existing review for this chart
                user_review = Review.objects.filter(
                    user=request.user, chart=chart).first()
                # if they do, pre-populate the form fields with this review
                if user_review:
                    data = {key: getattr(user_review, key)
                            for key in ['text',
                                        'clear_rating',
                                        'hc_rating',
                                        'exhc_rating',
                                        'score_rating',
                                        'characteristics',
                                        'recommended_options']}
                    form = ReviewForm(data)

                # if they don't, create a blank form
                else:
                    form = ReviewForm()
            context['form'] = form

    # get reviews for this chart and assemble display info for said reviews
    # TODO fix line length
    chart_reviews = Review.objects.filter(chart=chart).prefetch_related('user__userprofile')
    context['reviews'] = [{
                              'user': review.user.get_username(),
                              'user_id': review.user.id,
                              'playside': review.user.userprofile.get_play_side_display(),
                              'text': review.text,
                              'clear_rating': review.clear_rating,
                              'hc_rating': review.hc_rating,
                              'exhc_rating': review.exhc_rating,
                              'score_rating': review.score_rating,
                              'characteristics': ', '.join([
                                  TECHNIQUE_CHOICES[x][1] for x in
                                  review.characteristics]),
                              'recommended_options': ', '.join([
                                  RECOMMENDED_OPTIONS_CHOICES[x][1] for x in
                                  review.recommended_options])
                          } for review in chart_reviews]

    # assemble page title
    context['page_title'] = 'STATISTIK // ' + context['title']
    return render(request, 'chart.html', context)


def elo_view(request):
    win = request.GET.get('win')
    lose = request.GET.get('lose')
    level = request.GET.get('level')

    is_hc = int(request.GET.get('hc', 0))
    # TODO extend to accommodate exhc and score types
    rating_type = 1 if is_hc else 0
    elo_type = 'elo_rating_hc' if is_hc else 'elo_rating'
    type_display = 'HC' if is_hc else 'NC'

    if not level:
        return HttpResponseBadRequest()

    # handle incoming elo reviews
    # TODO don't use GET for this
    if win and lose:
        with transaction.atomic():
            win_chart = Chart.objects.get(pk=int(win))
            lose_chart = Chart.objects.get(pk=int(lose))
            drawn = bool(request.GET.get('draw'))

            # elo magic happens here
            elo_env = elo.Elo(k_factor=20)
            win_chart_elo = getattr(win_chart, elo_type)
            lose_chart_elo = getattr(lose_chart, elo_type)
            win_rating, lose_rating = elo_env.rate_1vs1(win_chart_elo,
                                                        lose_chart_elo,
                                                        drawn=drawn)

            # update charts with new elo ratings
            setattr(win_chart, elo_type, win_rating)
            setattr(lose_chart, elo_type, lose_rating)
            win_chart.save()
            lose_chart.save()

            # record review in case ratings need to be regenerated
            EloReview.objects.create(first=win_chart,
                                     second=lose_chart,
                                     drawn=drawn,
                                     type=rating_type)
        return HttpResponseRedirect(reverse('elo') + '?level=%s&hc=%s' %
                                    (level, rating_type))

    # handle regular requests
    else:
        display_list = bool(request.GET.get('list'))
        if display_list:
            # display list of charts ranked by elo
            # TODO fix line length
            matched_charts = Chart.objects.filter(difficulty=int(level), type__lt=3).prefetch_related('song').order_by('-' + elo_type)

            # assemble displayed elo info for matched charts
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
    user = User.objects.filter(pk=request.GET.get('id')).first()
    if user:
        # get all reviews created by this user
        matched_reviews = Review.objects.filter(user=user).prefetch_related('chart__song')
        # assemble display info for these reviews
        # TODO fix line length
        context['reviews'] = [{
                                  'title': review.chart.song.title,
                                  'text': review.text,
                                  'chart_id': review.chart.id,
                                  'type_display': review.chart.get_type_display(),
                                  'difficulty': review.chart.difficulty,
                                  'clear_rating': review.clear_rating,
                                  'hc_rating': review.hc_rating,
                                  'exhc_rating': review.exhc_rating,
                                  'score_rating': review.score_rating,
                                  'characteristics': ', '.join([
                                      TECHNIQUE_CHOICES[x][1] for x in
                                      review.characteristics]),
                                  'recommended_options': ', '.join([
                                      RECOMMENDED_OPTIONS_CHOICES[x][1]
                                      for x in review.recommended_options])
                              } for review in matched_reviews]

        # assemble page title
        context['title'] = ' // '.join([user.username.upper(), 'REVIEWS'])
        context['page_title'] = 'STATISTIK // ' + context['title']

        return render(request, 'user.html', context)

    else:
        # return list of all registered users
        users = User.objects.filter(is_superuser=False).prefetch_related('userprofile')
        # assemble display info for users
        # TODO fix line length
        context['users'] = [{
                                'user_id': user.id,
                                'username': user.username,
                                'dj_name': user.userprofile.dj_name,
                                'playside': user.userprofile.get_play_side_display(),
                                'best_techniques': ', '.join([TECHNIQUE_CHOICES[x][1] for x in user.userprofile.best_techniques]),
                                'max_reviewable': user.userprofile.max_reviewable,
                                'location': user.userprofile.location
                            } for user in users]

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
            user = User.objects.create_user(username=data.get('username'),
                                            password=data.get('password'),
                                            email=data.get('email'))
            user.save()
            user_profile = UserProfile(user_id=user.id,
                                       dj_name=data.get('dj_name').upper(),
                                       location=data.get('location'),
                                       play_side=data.get('playside'),
                                       best_techniques=data.get('best_techniques'),
                                       max_reviewable=0)
            user_profile.save()

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
