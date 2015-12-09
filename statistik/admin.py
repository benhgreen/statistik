from django.contrib import admin
from statistik.models import UserProfile, Chart, Song, Review, EloReview

admin.site.register(UserProfile)
admin.site.register(Chart)
admin.site.register(Song)
admin.site.register(Review)
admin.site.register(EloReview)