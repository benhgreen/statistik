#!/bin/bash -e

echo Waiting for DB to be available... 
while ! nc -z db 5432 2>/dev/null
do
    let elapsed=elapsed+1
    if [ "$elapsed" -gt 90 ] 
    then
        echo "TIMED OUT !"
        exit 1
    fi  
    sleep 1;
done

python3 manage.py migrate
python3 misc/import_music_csv.py
# python3 misc/import_chart_csv.py
python3 manage.py runserver 0.0.0.0:8000