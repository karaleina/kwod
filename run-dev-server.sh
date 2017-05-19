#!/bin/sh

# Doklejam katalog z projektem do listy sciezek (zmiennej srodowiskowej PYTHONPATH),
# w ktorej python wyszukuje pakiety
export PYTHONPATH=$PYTHONPATH:.

# Mowie flaskowi tu jest aplikacja
export FLASK_APP=kwod_webapp.webapp

# Ma wypisywac informacje debugowe
export FLASK_DEBUG=1
flask run --host 0.0.0.0
