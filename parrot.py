#!/usr/bin/env python3


import argparse
import getopt
import json
import os
import requests
import random
import sys
import string

GITHUB_API="https://api.github.com"


def main(site, username, read):
	if read:
		readPass(site)
	else:
		writePass(username, site)


def readPass(site):
	try:
		headers = {'Authorization':f'token {git_token}'}
		params = {'username': git_username, 'filename': f'PARROT_PASSWORD_{site}'}
		#res = requests.get(GITHUB_API+'/search/gists', headers=headers, params=params)
		res = requests.get(f'{GITHUB_API}/gists', headers=headers, params=params)
		j = json.loads(res.text)
		for gist in j:
			if f'PARROT_PASSWORD_{site}' in gist['files'].keys():
				cred_dict = gist['files'][f'PARROT_PASSWORD_{site}']
				res = requests.get(cred_dict['raw_url'], headers=headers)
				creds = res.text.split(':')
				print(f'Retrieved credentials for {site} from gist.github.com')
				print(f'username: {creds[0]}')
				print(f'password: {creds[1]}')
				print(f"gist ID: {gist['id']}")		
	#	gist_id = res.body.items[0].id
	# 	res = requests.get(f'{GIT_URL}/gists/{gist_id}', headers=header)
	# 	content = res.files[0].content
	# 	creds = content.split(':')
	# 	print(f'username: {creds[0]}')
	# 	print(f'password: {creds[1]}')
	except Exception as e:
		print(f'Error Reading: {e}')


def writePass(username, site):
	try:
		password = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
		headers = {'Authorization':f'token {git_token}'}
		params = {'scope':'gist'}
		payload = {'description':'PARROT PASSWORD','public':True,'files':{f'PARROT_PASSWORD_{site}':{'content':f'{username}:{password}'}}}
		res = requests.post(f'{GITHUB_API}/gists', headers=headers, params=params,data=json.dumps(payload))
		j = json.loads(res.text)
		print(f"Gist saved with ID {j['id']} at {j['html_url']}")
		print(f"Password is {password}")
	except Exception as e:
		print(f'Error Writing: {e}')

if __name__ == '__main__':
	git_token = os.environ['PARROT_TOKEN']
	git_username = os.environ['PARROT_USERNAME']

	parser = argparse.ArgumentParser(description='Parrot Password Manager. Don\'t actually use this. Seriously. ')
	parser.add_argument('-s', dest='site', action='store',default=None,help='REQUIRED: Site name/Account description (for example Paypal, Amex, Youtube)')
	parser.add_argument('-u', dest='username', action='store',default=None,help='REQUIRED: Username for the account you want to generate a password for')
	parser.add_argument('-r', dest='read', action='store_true', default=None,help='Read Password from github')
	parser.add_argument('-w', dest='read', action='store_false',default=None,help='Write Password to github')
	args = parser.parse_args()
	site = args.site
	username = args.username
	read = args.read

	if read is not None and site is not None and ((not read and username is not None) or read):
		main(site, username, read)
	else:
		print('learn to read asshole.')