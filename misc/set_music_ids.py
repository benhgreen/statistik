from statistik.models import Song

for song in Song.objects.all():
    song.music_id = song.id
    song.save()
