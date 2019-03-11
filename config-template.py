#!/usr/bin/env python

import argparse, os, logging, json
from jinja2 import Template

parser = argparse.ArgumentParser(epilog="""
The complete environment will be loaded by default.
To limit to specific environment variables use the --env flag.
""")

parser.add_argument('-t', '--template', required=True, help='A configuration template')
parser.add_argument('-o', '--output', required=True, help='A path to write the rendered configuration to')

parser.add_argument('-e', '--env', action='append', metavar='ENV_VAR', help='One or more environment variable to load')
parser.add_argument('-f', '--file', action='append', metavar='FILE_PATH', help='One or more file to load as text')
parser.add_argument('-j', '--json', action='append', metavar='JSON_PATH', help='One or more JSON file to load as an object each')

parser.add_argument("-l", "--loglevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='WARNING', help="Set the logging level, default: %(default)s")
parser.add_argument('--version', action='version', version=os.getenv('CONFIG_TEMPLATE_VERSION'))

args = parser.parse_args()

logging.basicConfig(level=getattr(logging, args.loglevel))

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
			with open(k) as valueFile:
				data['file'][filename.replace('.','_')] = valueFile.read()
		except FileNotFoundError as error:
				logging.warning(error)

data['json'] = dict()
if args.json:
	for k in args.json:
		dummy, filename = os.path.split(k)
		try:
			with open(k) as valueFile:
				data['json'][filename.replace('.','_')] = json.load(valueFile)
		except FileNotFoundError as error:
				logging.warning(error)

logging.debug("data object:%s", data)

with open(args.template) as templateFile:
    template = Template(templateFile.read())
template.stream(data).dump(args.output)

logging.info("configuration template completed")