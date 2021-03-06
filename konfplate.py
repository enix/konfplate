#!/usr/bin/env python

import argparse, os, logging, json, sys
from jinja2 import Template

parser = argparse.ArgumentParser()

parser.add_argument('-t', '--template', default="-", help='A configuration template')
parser.add_argument('-o', '--output', default="-", help='A path to write the rendered configuration to')

parser.add_argument('-e', '--env', action='append', metavar='ENV_VAR', help='One or more environment variable to load (default: load the complete environment)')
parser.add_argument('-f', '--file', action='append', metavar='FILE_PATH', help='One or more file to load as text')
parser.add_argument('-j', '--json', action='append', metavar='JSON_PATH', help='One or more JSON file to load as an object each')

parser.add_argument("-d", "--debug", action='store_true', help="Enable debug mode")

args = parser.parse_args()

if args.debug:
	logging.basicConfig(level=logging.DEBUG)
else:
	logging.basicConfig(level=logging.INFO)

logging.debug("args:%s", args)

data = dict()

if args.env:
	data['env'] = dict()
	for k in args.env:
		if k in os.environ:
			data['env'][k] = os.environ[k]
		else:
			logging.warning("Environment variable not found: %s", k)
else:
	data['env'] = os.environ

data['file'] = dict()
if args.file:
	for k in args.file:
		dummy, filename = os.path.split(k)
		try:
			with open(k) as valuefile:
				data['file'][filename.replace('.','_')] = valuefile.read()
		except FileNotFoundError as error:
				logging.warning(error)

data['json'] = dict()
if args.json:
	for k in args.json:
		dummy, filename = os.path.split(k)
		try:
			with open(k) as valuefile:
				data['json'][filename.replace('.','_')] = json.load(valuefile)
		except FileNotFoundError as error:
				logging.warning(error)

logging.debug("Template Environment: %s", data)

with sys.stdin if args.template == "-" else open(args.template) as templatefile:
    template = Template(templatefile.read())
template.stream(data).dump(sys.stdout if args.output == "-" else args.output)

logging.info("configuration template rendered")