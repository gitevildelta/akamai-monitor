#!/usr/bin/env python

from base64 import b64encode
from hashlib import sha512
import requests
import struct
import time
import json
import re

SETTINGS_FILENAME = 'settings.json'

AKAMAI_SCRIPT_REGEX = r'<script\s+type="text/javascript"\s+src="([^"]+)">\s*</script>\s*</body>'
AKAMAI_SCRIPT_REGEX_PATH_GROUP = 1

def read_settings():
	with open(SETTINGS_FILENAME, 'rt') as src:
		serialized = src.read()
	return json.loads(serialized)

"""
Download the Akamai script
"""
def download_akamai_script(target):
	session = requests.Session()
	session.headers = {
		'Accept': '*/*',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:106.0) Gecko/20100101 Firefox/106.0',
		'Accept-Language': 'fr-FR,fr;q=0.5'
	}
	page = session.get(target)

	# Get scheme (http/https) and the host.
	target_url_match = re.search(r'^(https?)://([^/]+)/.*', page.url)
	target_scheme = target_url_match.group(1)
	target_host = target_url_match.group(2)

	# Find Akamai script
	akamai_script_path_match = re.search(AKAMAI_SCRIPT_REGEX, page.text)
	if akamai_script_path_match == None:
		return None
	akamai_script_path = akamai_script_path_match.group(AKAMAI_SCRIPT_REGEX_PATH_GROUP)

	if len(akamai_script_path) == 0 or akamai_script_path[0] != '/':
		raise Exception(f'Empty or invalid Akamai Script Path : "{akamai_script_path}"')

	akamai_script_response = session.get(f'{target_scheme}://{target_host}{akamai_script_path}')
	return akamai_script_response.text

"""
Compute the checksum of the given script.

This implementation compute the checksum using SHA-512 and append the length of the script at the end
"""
def compute_checksum(script):
	sha512_digest = sha512(script.encode('utf-8')).digest()
	length_bytes = struct.pack('!i', len(script))
	return sha512_digest + length_bytes

while True:
	settings = read_settings()
	target = settings['target']
	delay_seconds = settings['delay']

	print(f'Checking {target}')

	akamai_script = download_akamai_script(target)
	checksum = compute_checksum(akamai_script)

	print(checksum.hex())

	print('Sleeping {delay_seconds} seconds.')
	time.sleep(delay_seconds)
