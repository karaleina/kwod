# -*- coding: utf-8 -*-

# Obiekt bazy danych skonfigurowany przez aplikację
from kwod_webapp.database.models import *

# klasa reprezentująca datę wraz z godziną
from datetime import datetime

def searchInDb( pesel, recordingDate ):

	recordings = ECGRecording.query
	if isinstance(pesel, basestring):
		recordings.join(ECGRecording.patient).filter(ECGPatient.pesel.like('%' + pesel + '%'))
	if isinstance(recordingDate, datetime):
		recordings.filter(ECGRecording.timestamp == recordingDate)
# 		print("byDate")
		
# 	print(type(recordingDate))	
	print(recordings)
	for r in recordings:
		print(r.name)
	return
	

def findOrCreateNewPatient(patientName, patientSurname, db):

    patient = ECGPatient.query.filter(ECGPatient.name == patientName).filter(ECGPatient.surname == patientSurname).first()
    if not patient:
        patient = ECGPatient(name=patientName, surname=patientSurname)
        db.session.add(patient)
        db.session.commit()

    return patient
# przykład użycia
# searchInDb("1", datetime(2015, 6, 12))