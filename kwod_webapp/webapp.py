# -*- coding: utf-8 -*-

# Flask to  jest framework (biblioteka) do aplikacji webowych. (Flask to klasa pakietu flask).
# render_template to funkcja, która na podstawie szablonu generuje html (importujemy konkretną funkcję z Flaska).
import os
from datetime import datetime
from flask import Flask, jsonify, render_template, request
from wfdbtools import rdann, rdsamp
from flask import url_for
from werkzeug.utils import secure_filename, redirect

from kwod_webapp.algorithms.r_wave_detection import algorithms
from kwod_webapp.parsers.header_parser import HeaderParser
from kwod_webapp.database.configuration import db
from kwod_webapp.database.models import ECGPatient, ECGRecording
from kwod_webapp.medical import qrs_detector, qrs_compare
from kwod_webapp.parsers.ecg_recording_data_parser import ECGRecordingDataParser
from kwod_webapp.database.db_search import findOrCreateNewPatient
from math import nan
# Konstruktor klasy Flask - reprezentuje aplikację webową
app = Flask(__name__)

# Mówimy, jaka to baza danych (sqlite) i mówimy gdzie ona jest
# (lub ma być, bo jak nie ma to tworzymy)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecg-database.sqlite'

UPLOAD_FOLDER = 'downloads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Przypisuje aplikację do bazy danych.
db.app = app
db.init_app(app)
# Udostępniam innym modułom, innemu kodowi bazę danych z przypisaną już aplikacją
db_in_app = db

# "Małpka" = dekorator
# @app.route(<url>) - Widok dla konkretnego adresu url
# "/" oznacza url (widok) główny
@app.route("/")
def recording_list():
    # Pobiera z bazy wszystkie rekordy ECG i zwraca jako tablica obiektów tej samej klasy
    # Query to zapytanie do bazy danych = "daj mi wszystkie rekordingi jakie są w bazie"
    name = request.args.get('name')
    surname = request.args.get('surname')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    recordings = db.session.query(ECGRecording).join(ECGPatient)

    if name:
        recordings = recordings.filter(ECGPatient.name == name)
    if surname:
        recordings = recordings.filter(ECGPatient.surname == surname)
    if from_date:
        recordings = recordings.filter(ECGRecording.timestamp >= from_date)
    if to_date:
        recordings = recordings.filter(ECGRecording.timestamp <= to_date)

    # Renderuje html na podstawie szablonu
    return render_template('main.html', recordings=recordings.all())


@app.route("/recordings/<int:recording_id>/view")
def show_recording(recording_id):
    # Tutaj pobieram z bazy rekord o zadanym id i dostaję obiekt
    recording = ECGRecording.query.get(recording_id)
    recording_data_with_time = get_raw_recording_data(recording, 0, 10)
    true_qrs_with_time = get_recording_true_qrs_with_time(recording)

    r_waves_from_algorithms = calculate_qrs_labels(recording, recording_data_with_time)

    RR_means = {
        algorithm_name: calculate_rr(recording.plot_count, r_waves_from_algorithms[algorithm_name])
        for algorithm_name, labels in r_waves_from_algorithms.items()
    }

    quality = {
       algorithm_name: calculate_quality(recording.plot_count, true_qrs_with_time, r_waves_from_algorithms[algorithm_name])
       for algorithm_name, labels in r_waves_from_algorithms.items()
       }

    print(quality)

    return render_template(
        'ecg_view.html',
        recording=recording,
        recording_data=recording_data_with_time,
        r_waves_from_algorithms=r_waves_from_algorithms,
        RR_means=RR_means

    )

@app.route("/new_patient", methods=['POST'])
def new_recording():
    name = request.form['name']
    surname = request.form['surname']
    # file_header = request.args.get('fileHeader')
    # file_dat = request.args.get('fileDat')

    if request.method == 'POST':

        file = request.files['fileHeader']
        fileDat = request.files['fileDat']

        if file and fileDat:
            filename = secure_filename(file.filename)
            # zapisujemy plik pod sciezka (katalog projektu)/downloads/nazwapliku.header
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenameDat = secure_filename(fileDat.filename)
            fileDat.save(os.path.join(app.config['UPLOAD_FOLDER'], filenameDat))

            header_parser = HeaderParser()
            patient = findOrCreateNewPatient(name, surname, db_in_app)
            patient.recordings.append(header_parser.parse_header(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            db_in_app.session.commit()

            res = redirect("/")
            res.data = ""
            return res
        else :
            res = redirect("/")
            res.data = ""
            return res

# Widok służący do zwracania danych z danego przedziału czasu
@app.route("/recordings/<int:recording_id>")
def get_recording_data(recording_id):
    start_time = int(request.args.get('from'))
    end_time = int(request.args.get('to'))

    recording = ECGRecording.query.get(recording_id)
    recording_data_with_time = get_raw_recording_data(recording, start_time, end_time)
    r_waves_from_algorithms = calculate_qrs_labels(recording, recording_data_with_time)
    RR_means = {
        algorithm_name: calculate_rr(recording.plot_count, r_waves_from_algorithms[algorithm_name])
        for algorithm_name, labels in r_waves_from_algorithms.items()
    }

    return jsonify({
        "recordingData": recording_data_with_time,
        "r_waves_from_algorithms": r_waves_from_algorithms,
        "RR_means": RR_means
    })


def calculate_rr(plot_count, labels):
    czasy_zalamkow_rr_per_plot = [[] for i in range(0, plot_count)]
    for zalamek in labels:
        if zalamek['type'] == 'R':
            plot_zalamka = zalamek['plotId']
            czas_zalamka = zalamek['time']
            czasy_zalamkow_rr_per_plot[plot_zalamka].append(czas_zalamka)
    return [rr_means_info(float(sum_of_differences(czasy_zalamkow)) / float(len(czasy_zalamkow)-1))
            for czasy_zalamkow in czasy_zalamkow_rr_per_plot]




def calculate_quality(plot_count, raw_R_waves_time,  labels):
    czasy_zalamkow_rr_per_plot = [[] for i in range(0, plot_count)]
    for zalamek in labels:
        if zalamek['type'] == 'R':
            plot_id = zalamek['plotId']
            czas_zalamka = zalamek['time']
            czasy_zalamkow_rr_per_plot[plot_id].append(czas_zalamka)

    compare = qrs_compare.QRSCompare()
    [sensitivity, specifity] = compare.compare_segmentation(raw_R_waves_time, czasy_zalamkow_rr_per_plot[plot_id])
    return [rr_quality_info(sensitivity, specifity)]


def rr_quality_info(sensitivity, specifity):

    return {
        'sensitivity': sensitivity,
        'specifity': specifity
    }



def rr_means_info(rr_means):

    if rr_means == 0:
        return {
            'distance': 'brak danych',
            'frequency': 'brak danych',
            'diagnosis': 'brak danych'
        }
    else:
        if 60.0/rr_means > 100:
            return {
                'distance': rr_means,
                'frequency': 60.0 / rr_means,
                'diagnosis': 'tachykardia'
            }
        if 60.0/rr_means < 60 :
            return {
                'distance': rr_means,
                'frequency': 60.0 / rr_means,
                'diagnosis': 'bradykardia'
            }
        else:
            return {
                'distance': rr_means,
                'frequency': 60.0 / rr_means,
                'diagnosis': 'norma'
        }

def sum_of_differences(array):
    sum = 0
    for i in range(1, len(array)):
        sum += array[i] - array[i-1]
    return sum

def get_raw_recording_data(recording, start_time, end_time):
    from_sample = max(0, start_time * recording.frequency)
    to_sample = min(recording.sample_count - 1, end_time * recording.frequency)

    recording_data = ECGRecordingDataParser().parse(recording.url, from_sample, to_sample)
    recording_data_with_time = [
        [(from_sample + index) / float(recording.frequency)] + recording_data_sample
        for index, recording_data_sample in enumerate(recording_data)]

    return recording_data_with_time

def rTimeWaves(path_string, stop_sample):

    result_qrs = rdann(path_string, 'qrs', start=0, end=stop_sample, types=[])
    r_waves = []

    for element in result_qrs:
        if element[1] <= stop_sample:
            r_waves.append(element[1])
        else:
            break

    return r_waves

def get_recording_true_qrs_with_time(recording):
     url = getattr(recording, "url")
     head = os.path.splitext(url)[0]
     return rTimeWaves(head, 10^5)

def calculate_qrs_labels(recording, recording_data_with_time):
    algorithm_results = {}

    for algorithm in algorithms:
        r_waves = []

        for plot_id in range(0, recording.plot_count):
            recording_data_for_plot = [
                recording_data_with_time[i][plot_id + 1]
                for i in range(0, len(recording_data_with_time))]
            zalamki_r = algorithm.detect_r_waves(recording_data_for_plot)
            for zalamek_r in zalamki_r:
                r_waves.append({"plotId": plot_id, "type": "R", "time": recording_data_with_time[zalamek_r][0]})

        print("Typ: ", type(r_waves))
        algorithm_results[algorithm.name()] = r_waves
    return algorithm_results


# Uruchamia aplikację, jeśli plik nie jest importowany, tylko uruchamiany
if __name__ == "__main__":
    app.run()
