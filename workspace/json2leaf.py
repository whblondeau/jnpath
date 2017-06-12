#!/usr/bin/python

# Ehhh. Gonna port this to Python 2 for now...


# -------------------------------------------------------------- FUNCTIONS


def is_number(val):

    if isinstance(val, int):
        return True

    if isinstance(val, float):
        return True

    try:
        float(val)
        return True
    except ValueError:
        pass

    try:
        int(val)
        return True
    except ValueError:
        pass

    return False


def normalize_whitespace(str):
    import re
    str = str.strip()
    str = re.sub(r'\s+', ' ', str)
    return str


def prepare_leaf_value(leaf_val):

    if isinstance(leaf_val, bool):
        if leaf_val:
            return unicode('true')
        else:
            return unicode('false')

    elif isinstance(leaf_val, str):
        #escape the fucking newlines
        leaf_val = leaf_val.replace('\n', newline_escape)
        return unicode(leaf_val)

    elif isinstance(leaf_val, unicode):
        leaf_val = leaf_val.replace('\n', newline_escape)
        return leaf_val

    elif is_number(leaf_val):
        return unicode(leaf_val)

    elif leaf_val is None:
        return unicode('null')

    elif isinstance(leaf_val, list):
        return unicode('[]')

    elif isinstance(leaf_val, dict):
        return unicode('{}')

    else:
        print('WTF!!!' + str(type(leaf_val)))
        exit(0)


def enumerate_leafpaths(current_node, current_pathstring='', current_steplist=[]):
    '''This function accepts a parsed JSON object and returns
    a 3-tuple of all leaf paths in the instance. The 3-tuple
    is of the form (pathstring, steplist, leafnode).
    Note that pathstring and steplist are logically equivalent. This method
    provides both because they afford different conveniences for
    the various JSNPath evaluation techniques that will operate on these
    leafpaths.'''

    # children to iterate through?
    if isinstance(current_node, list):
        if not current_node:
            # empty list. This is a leaf. Give it up.
            yield (current_node, current_pathstring, current_steplist)
        else:
            for indx, val in enumerate(current_node):
                childpath = current_pathstring + '[' + str(indx) + ']'
                # make a separate copy!
                childsteplist = copy.copy(current_steplist)
                childsteplist.append(str(indx))
                result = enumerate_leafpaths(val, childpath, childsteplist)
                for item in result:
                    # result best be nested iterators of tuples!
                    yield item

    elif isinstance(current_node, dict):
        if not current_node:
            # empty dict. This too is a leaf. Give it up.
            yield (current_node, current_pathstring, current_steplist)
        else:
            for attrname in current_node:
                val = current_node[attrname]
                childpath = current_pathstring + '[\'' + attrname + '\']'
                # make a separate copy!
                childsteplist = copy.copy(current_steplist)
                childsteplist.append(attrname)
                result = enumerate_leafpaths(val, childpath, childsteplist)
                for item in result:
                    # result best be nested iterators of tuples!
                    yield item

    else:
        leafpath = (current_node, current_pathstring, current_steplist)
        yield leafpath


def paths_dict(jsonobj):
    '''accepts a compiled json object and 
    returns a dictionary whose keys are string 
    representations of jnpaths and whose values are
    leaf nodes.
    '''
    # get a generator of 3-tuple path info
    leafpaths = enumerate_leafpaths(jsonobj)

    pathdict = {}

    for noderep in leafpaths:
        pathstring = noderep[1]
        pathdict[pathstring] = noderep[0]

    return pathdict


# -------------------------------------------------------------- CONSTANTS

newline_escape = '\q'

usage = '''USAGE:

    json2leaf --help | <serialized json obj>

This script accepts a json serialization and returns a sorted
leafpath representation of all content.

The returned lines are separated by newlines. 

Each line is of the form [id][id][id]...|||leaf-value||| The extravagant
delimiter around the leaf-value is because leaf values, unlike path step
ids, are problematic and likely to contain all kinds of crap, including
expressions that might break data escapes. The "|||" literal is
expected to be reasonably safe in this respect. Other delimiter literals
can be used if needed.

The one weird substitution in leaf content, primarily to support 
line-mode output, is that newline "\n" character sequences (which are
converted to actual newline sequences when printing to stdout) are
replaced by "\q", which hopefully will not get sideways
with any parameter passing or text processing. It's the responsibility
of the calling code to restore (or remove) these doubly escaped newlines.
'''

# -------------------------------------------------------------- EXECUTE

import sys
import json
import copy

if '--help' in sys.argv:
    print(usage)
    exit(0)

if len(sys.argv) < 2:
    print('ARGUMENT REQUIRED.')
    print(usage)
    exit(1)

leaf_open_demarc = '|||'
leaf_end_demarc = '|||'

jsoncontent = sys.argv[1]

# print(jsoncontent)

jsonobj = None

try:
    jsonobj = json.loads(jsoncontent)
except Exception as ex:
    print('CANNOT PARSE ARGUMENT:')
    print(ex)
    exit(1)

pathdict = paths_dict(jsonobj)

# output
for path in sorted(pathdict.keys()):

    leaf = prepare_leaf_value(pathdict[path])
    if leaf is None:
        leaf = ''

    line = path + leaf_open_demarc + leaf + leaf_end_demarc
    print line

