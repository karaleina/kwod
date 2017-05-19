# -*- coding: utf-8 -*-

from kwod_webapp.database.configuration import db


# Klasa ECGRecording, która dziedziczy po klasie Model
class ECGRecording(db.Model):
    __tablename__ = 'ecgrecording'

    # Pola w klasie, czyli w tym przypadku kolumny w tabeli:

    # Kolumna typu integer - identyfikator danego przebiegu EKG -
    # klucz główny "primary key"
    id = db.Column(db.Integer, primary_key=True)

    # Kolumna typu string (to może być nazwa, opis)
    name = db.Column(db.String(1024))

    # Kolumna typu czas (np data badania)
    timestamp = db.Column(db.DateTime())

    # Kolumna typu string (ścieżka do pliku z danymi)
    url = db.Column(db.String(1024))

    # Kolumna typu integer - liczba plotów
    plot_count = db.Column(db.Integer)

    # Kolumna typu integer - częstotliwość próbkowania
    frequency = db.Column(db.Integer)

    # Kolumna typu integer - liczba próbek w recordingu
    sample_count = db.Column(db.Integer)

    # Kolumna typu string - komentarz do badania
    comment = db.Column(db.String(16384))

    id_patient = db.Column(db.Integer, db.ForeignKey('ecgpatient.id'))

    # Konstruktor który służy do dodawania rzeczy do bazy danych
    def __init__(self, name, timestamp, url, plot_count, frequency, sample_count, comment):
        self.name = name
        self.timestamp = timestamp
        self.url = url
        self.plot_count = plot_count
        self.frequency = frequency
        self.sample_count = sample_count
        self.comment = comment

    # Dzięki tej metodzie można wypisywać obiekty na konsolę jako string
    def __repr__(self):
        return '<ECGRecording %s>' % self.name


# Klasa ECGRecording, która dziedziczy po klasie Model
class ECGPatient(db.Model):
    __tablename__ = 'ecgpatient'

    # Pola w klasie, czyli w tym przypadku kolumny w tabeli:

    # Kolumna typu integer - identyfikator danego przebiegu EKG -
    # klucz główny "primary key"
    id = db.Column(db.Integer, primary_key=True)

    # Kolumna typu string (to może być nazwa, opis)
    name = db.Column(db.String(1024))
    surname = db.Column(db.String(1024))
    recordings = db.relationship("ECGRecording", backref="patient")

    # Konstruktor który służy do dodawania rzeczy do bazy danych
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    # Dzięki tej metodzie można wypisywać obiekty na konsolę jako string
    def __repr__(self):
        return '<ECGPacjent %s>' % (self.name + " " + self.surname)
