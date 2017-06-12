#!/usr/bin/python


usage = '''USAGE: python addleaf-json.py path leafval [json]

PARAMETERS:

    `path`: the path expression in [] notation

    `leafval`: the value that terminates the path

    `json`: serialized JSON or path to JSON file. If omitted, 
        this script builds an empty JSON container (array or
        object) and adds the leafpath + value to it.
'''

import sys
import json
import os, os.path

if '--help' in sys.argv:
    print(usage)
    exit(0)

if len(sys.argv) < 3:
    print('TWO ARGUMENTS REQUIRED.')
    print(usage)
    exit(1)

pathparam = sys.argv[1]
leafvalparam = sys.argv[2]
jsonparam = None

if len(sys.argv) > 3:
    jsonparam = sys.argv[3]

jsonobj = None
jsoncontent = None

if os.path.isfile(jsonparam):
    print('Reading JSON content from file ' + jsonparam + '.')
    with open(jsonparam) as srcfile:
        jsoncontent = srcfile.read()
else:
    print('Parsing parameter as JSON content.')
    jsoncontent = jsonparam
