import re
from datetime import datetime


def parse_ssh_log(log_line):
    match = re.search(r'Failed password for .*? user (.*?) from ([\d\.]+) port', log_line)
    if match:
        timestamp_str = ' '.join(log_line.split(' ')[0:3])

        # Get current year
        current_year = datetime.now().year

        # Include year information in the date conversion
        try:
            timestamp = datetime.strptime(f"{current_year} {timestamp_str}", '%Y %b %d %H:%M:%S')
        except ValueError:
            # If the log file is from the year before the current year,
            # we can try to parse it from the previous year. This is a higher-level control.
            timestamp = datetime.strptime(f"{current_year - 1} {timestamp_str}", '%Y %b %d %H:%M:%S')

        return {
            'type': 'ssh_failed_login',
            'timestamp': timestamp,
            'username': match.group(1),
            'ip_address': match.group(2),
            'raw_log': log_line.strip()
        }
    return None