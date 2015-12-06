from django.conf import settings
from statistik.models import EloReview
import elo

for review in EloReview.objects.all():
    song1 = review.first
    song2 = review.second

    elo_env = elo.Elo(k_factor=25)

    elo_type = 'elo_rating_hc' if review.type else 'elo_rating'
    song1_elo = getattr(song1, elo_type)
    song2_elo = getattr(song2, elo_type)

    rate1, rate2 = elo_env.rate_1vs1(song1_elo,
                                     song2_elo,
                                     drawn=review.drawn)

    setattr(song1, elo_type, rate1)
    setattr(song2, elo_type, rate2)

    song1.save()
    song2.save()
