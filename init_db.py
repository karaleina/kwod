# -*- coding: utf-8 -*-
# Ten skrypt tworzy bazę danych. Jest wywoływany tylko raz.
import os

# "Gwiazdka" (*) importuje wszystko z danego pliku
# w tym przypadku wszystkie modele
from kwod_webapp.database.models import *

# Obiekt bazy danych skonfigurowany przez aplikację
from kwod_webapp.parsers.header_parser import HeaderParser
from kwod_webapp.webapp import db_in_app


# Stworzenie tabel bazodanowych
db_in_app.create_all()

patients = [
    ECGPatient(name='Jan', surname='Kowalski'),
    ECGPatient(name='Magda', surname='Jaka'),
    ECGPatient(name='Aleksandra', surname='Biomedyczna'),
    ECGPatient(name='Adam', surname='Malinowski'),
    ECGPatient(name='Marcin', surname='Mucha')
]

recordings_directory = "downloads/"
data_files = os.listdir(recordings_directory)

header_paths = [
    os.path.join(recordings_directory, data_file_path)
    for data_file_path in data_files
    if '.hea' in data_file_path]
    # if '.dat' in data_file_path]

print(data_files)

print(header_paths)
header_parser = HeaderParser()

for index, header_path in enumerate(header_paths):
    patient = patients[index % len(patients)]
    patient.recordings.append(header_parser.parse_header(header_path))


# Pętla po nagraniach, która dodaje kolejne rekordy do sesji (transakcji)
#  i jak już wszystkie doda, to robi commit i dodaje do bazy danych
for patient in patients:
    db_in_app.session.add(patient)
db_in_app.session.commit()
