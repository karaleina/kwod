# kwod

Projekt realizowany w ramach przedmiotu KWOD.
Aplikacja Web z bazą danych - przeglądarka przebiegów EKG
z detekcją załamków R i podstawową analizą odstępów RR.

## Instrukcje dla programistów

0. Wymagania

Zainstaluj Pythona 2.7.

1. Instalacja potrzebnych bibliotek

Wykonaj `pip install -r requirements.txt`.

2. Ściągnięcie plików z bazy Physionet

Wejdź do katalogu downloads/ i uruchom skrypt downloader.py.
Pobranie plików z bazy może potrwać kilka minut.

cd downloads/
python downloader.py

3. Inicjalizacja bazy danych

Wykonaj `python init_db.py`. Ten skrypt stworzy bazę
danych SQLite i załaduje do niej przykładowe dane.
Jeśli plik ten ulegnie modyfikacji należy skasować plik ecg-database.sqlite
i wygenerować go ponownie przy użyciu `python inint_db.py`

4. Uruchomienie aplikacji w trybie developerskim

W trybie developerskim wszystkie zmiany w kodzie powodują
automatyczne przeładowanie aplikacji. W katalogu głównym
przygotowane są dwa skrypty uruchamiające serwer w trybie
developerskim - po jednym dla Windowsa i Linuxa.

Windows: `run-dev-server.bat`

Linux: `./run-dev-server.sh`

5. Uruchomienie aplikacji w trybie produkcyjnym

Aby uruchomić aplikację, wykonaj `python -m kwod_webapp.webapp`.
Możesz ją otworzyć w przeglądarce wpisując w pasek adresu: http://localhost:5000/
