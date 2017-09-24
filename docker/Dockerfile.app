FROM statistik-requirements 
ENV PYTHONUNBUFFERED 1
ENV DATABASE_URL postgres://postgres:postgres@db:5432/postgres
ENV DJANGO_SETTINGS_MODULE docker.settings
ENV PGPASSWORD postgres
