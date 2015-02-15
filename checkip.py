# checkip
# Server IP check script

import re
import urllib;
from datetime import date

try:

	response = urllib.urlopen("http://checkip.dyndns.org")
	response_body = response.read()

	ip = re.search(r"([0-9]{1,3}\.){3}[0-9]{1,3}", response_body).group(0)
	print ip


except Exception as exc:
	print "Error:", exc
