import sys
import urllib.request

if len(sys.argv) < 2:
    print('Usage: python downloader.py RECNUMBER...')
    sys.exit(1)

numbers = sys.argv[1:]

extensions = ["hea", "qrs", "atr", "dat"]

for number in numbers:
    for extension in extensions:
        remote_url = 'https://www.physionet.org/physiobank/database/afdb/{number}.{ext}'.format(
            number=number, ext=extension)
        local_path = 'downloads/{number}.{ext}'.format(number=number, ext=extension)
        urllib.request.urlretrieve(remote_url, local_path)
