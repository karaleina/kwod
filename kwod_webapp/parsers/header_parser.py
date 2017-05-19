from time import strptime, mktime

from datetime import datetime

from kwod_webapp.database.models import ECGRecording


class HeaderParser(object):
    def __init__(self):
        pass

    def parse_header(self, header_url):
        with open(header_url, 'r') as f:
            first_line = f.readline()
            tokens = first_line.split()

            plot_count = int(tokens[1])

            comment_lines = []

            while True:
                line = f.readline()
                if not line:
                    break
                elif line.startswith("#"):
                    comment_lines.append(line[1:])

            return ECGRecording(
                name=tokens[0],
                timestamp=None,
                url=header_url.replace(".hea", ".dat"),
                plot_count=plot_count,
                frequency=int(tokens[2]),
                sample_count=int(tokens[3]),
                comment='\n'.join(comment_lines)
            )
