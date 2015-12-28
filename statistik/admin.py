from django.contrib import admin
from statistik.models import UserProfile, Chart, Song, Review, EloReview

admin.site.register(Chart)
admin.site.register(Song)
admin.site.register(Review)
admin.site.register(EloReview)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    exclude = ['best_techniques']
