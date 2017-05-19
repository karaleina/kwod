# -*- coding: utf-8 -*-

# db to jest odnośnik do bazy danych - obiekt klasy SQLAlchemy używany w wielu plikach
# (w modelach bazy danych, w aplikacji webowej, w skrypcie inicjalizującym bazę danych),
# dlatego jest zadeklarowany w osobnym pliku, bo inaczej "krzyżowe importy"

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
