#!/usr/bin/python


# -------------------------------------------------------------- COLORS

colors = {}
# ansi standard codes, with some nonconventional names
colors['nocolor'] = '\033[0m'
colors['red'] = '\033[31m'
colors['green'] = '\033[32m'
colors['dullyellow'] = '\033[33m'
# not legible on black screen background
colors['darkblue'] = '\033[34m'
colors['magenta'] = '\033[35m'
colors['cyan'] = '\033[36m'
# in cygwin, this is the default for uncolored text
colors['ltgray'] = '\033[37m'

# not standard ansi color codes: this syntax is an XTerm adaptation of ECMA-48 RGB coding.
colors['orange'] = '\033[38;2;255;111;0m'
colors['blue'] = '\033[38;2;64;127;255m'    # for visibility at commandline
colors['yellow'] = '\033[38;2;255;255;0m'
colors['brightwhite'] = '\033[38;2;255;255;255m'
colors['palegreen'] = '\033[38;2;162;255;192m'
colors['lightgreen'] = '\033[38;2;96;255;124m'
colors['lightred'] = '\033[38;2;255;112;192m'
colors['redorange'] = '\033[38;2;255;48;40m'    # for visibility at commandline
colors['lightredorange'] = '\033[38;2;255;96;70m'    # for visibility at commandline

colors['bold'] = '\033[1m'
colors['dim'] = '\033[2m'

# color convenience functions
def nocolor(thing):
    return colors['nocolor'] + str(thing) + colors['nocolor']

def red(thing):
    return colors['red'] + str(thing) + colors['nocolor']

def green(thing):
    return colors['green'] + str(thing) + colors['nocolor']

def dullyellow(thing):
    return colors['dullyellow'] + str(thing) + colors['nocolor']

def darkblue(thing):
    return colors['darkblue'] + str(thing) + colors['nocolor']

def magenta(thing):
    return colors['magenta'] + str(thing) + colors['nocolor']

def cyan(thing):
    return colors['cyan'] + str(thing) + colors['nocolor']

def ltgray(thing):
    return colors['ltgray'] + str(thing) + colors['nocolor']

def orange(thing):
    return colors['orange'] + str(thing) + colors['nocolor']

def blue(thing):
    return colors['blue'] + str(thing) + colors['nocolor']

def yellow(thing):
    return colors['yellow'] + str(thing) + colors['nocolor']

def brightwhite(thing):
    return colors['brightwhite'] + str(thing) + colors['nocolor']

def palegreen(thing):
    return colors['palegreen'] + str(thing) + colors['nocolor']

def lightgreen(thing):
    return colors['lightgreen'] + str(thing) + colors['nocolor']

def lightred(thing):
    return colors['lightred'] + str(thing) + colors['nocolor']

def redorange(thing):
    return colors['redorange'] + str(thing) + colors['nocolor']

def lightredorange(thing):
    return colors['lightredorange'] + str(thing) + colors['nocolor']

def bold(thing):
    return colors['bold'] + str(thing) + colors['nocolor']

def dim(thing):
    return colors['dim'] + str(thing) + colors['nocolor']



# -------------------------------------------------------------- FUNCTIONS

def err_out(msg):
    print(red(msg))
    print(dullyellow(usage))
    exit(1)


def eval_int(num):
    '''returns a tuple (is_integer, number val)'''
    try:
        val = int(num)
        return True, val
    except ValueError:
        return False, None


def pathstep_type(stepstring):
    '''Returns a tuple (is_named, is_index, numeric_val, list_length)'''

    if not stepstring.strip():
        # empty string
        raise ValueError('stepstring is empty or whitespace.')

    if stepstring.startswith('"') and stepstring.endswith('"'):
        return True, False, None, None

    elif stepstring.startswith("'") and stepstring.endswith("'"):
        return True, False, None, None

    else:
        # preserved list length information is expressed 
        # as '3 of 4', '7 of 9' etc. This guarantees that
        # order was preserved.
        # a single number indicates that list length was not
        # preserved 
        numbers = map(strip, stepstring.split('of'))

        list_length = None

        if len(step) > 1:
            # if not an int, list_length remains None
            list_length = eval_int(numbers[1])[1]

        is_integer, number_val = eval_int(numbers[0]):

        if is_integer:
            # gotta be an index
            return False, True, number_val, list_length
        else:
            raise ValueError('invalid stepstring: ' + stepstring + '.')


def regularize_index(indexnumber, list_length):
    '''This function returns an index unaltered if nonnegative,
    but converts negative indices into positive numbers corresponding
    to their position in a sequence of `list_length`.
    '''
    retval = None
    if indexnumber >= 0:
        return indexnumber
    else:
        return list_length - (indexnumber + 1)


def resolve_slice(index_matcher, checked_list_length):
    '''For an index_matcher that contains a ":". Returns a tuple of 
    (startswith, endsbefore) expressed as positive index values, and 
    reconciled with the list length.
    '''
    startswith, endsbefore = patternstep.slice(':')

    startswith = eval_int(startswith)
    if startswith[0]:
        if startswith[1] < 0:
            # it's a negative index, one-based counted from the end
            startswith[1] = regularize_index(startswith[1], checked_list_length)

    endsbefore = eval_int(endsbefore)
    if endsbefore[0]:
        if endsbefore[1] < 0:
            # it's a negative index, one-based counted from the end
            endsbefore[1] = regularize_index(endsbefore[1], checked_list_length)

    # is this index_matcher outsized for the list length?
    if endsbefore[1] >= checked_list_length:
        # deal with checked_list_length = 0
        endsbefore[1] = max(checked_list_length, 1)

    # coerce startswith to one less than endsbefore, IF NECESSARY to prevent
    # back-to-front arrangement. When startswith + 1 == endsbefore, the slice
    # selects absolutely nothing
    if startswith[1] >= endsbefore[1]:
        startswith[1] = endsbefore[1] -1

    return startswith[1], endsbefore[1]


def matches_index(numeric_pathval, index_matcher, checked_list_length):
    '''This function takes a pathstep number, an index_matcher expression,
    and a verified list length, and evaluates whether the pathval
    matches the index_matcher. Returns True if it does, else False.'''

    if ':' in index_matcher:
        # slice
        startswith, endsbefore = resolve_slice(index_matcher, checked_list_length)

        if numeric_pathval < startswith:
            # path index value before slice
            return False

        if numeric_pathval >= endsbefore:
            # path index value after slice
            return False

        return True


def is_stepmatch(pathstep, patternstep):
    ''' list_length is necessary if negative list indexes are
    being evaluated.'''

    if patternstep == '.':
        # anystep wildcard
        return True

    if pathstep == patternstep:
        # this takes care of named and index equality both
        return True

    # what kind of step?
    pathstep_is_named, pathstep_is_index, numeric_pathval, list_length = pathstep_type(pathstep)

    if pathstep_isindex:

        # sanity
        if list_length and list_length < 0:
            raise ValueError('list_length \'' + str(list_length) + '\' should not be negative.')

        if patternstep == '-':
            #index wildcard
            return True

        if ',' in patternstep:
            # It's a random sequence of index expressions. Bozhe moi.
            # make sure the whitespace is removed from each, then check.
            patternsteps =  map(strip, patternstep.split(','))

            for index_matcher in patternstep:
                if match_index(numeric_pathval, index_matcher, list_length):
                    return True




        else:
            # is it a sequence 


    elif pathstep_is_named:


    return False


def is_pathmatch(jnpath, jnpattern, path_start=0):
    '''jnpath and jnpattern must be in list(str) form.'''
    pathdx = path_start
    match = True

    for patternstep in jnpattern:
        current_pathstep = jnpath[pathdx]
        if stepmatch(current_pathstep, patternstep):
            pathdx += 1
        else:
            match = False
            break

    return match


def pathstring2list(pathstring):
    pathstring = pathstring.strip('[]')
    return pathstring.split('][')



# -------------------------------------------------------------- CONSTANTS


usage = '''USAGE:

    python path-match.py [--help] <jnpath> jnpattern>


'''


# -------------------------------------------------------------- EXECUTE

import sys

if '--help' in sys.argv:
    print(dullyellow(usage))
    exit(0)


call_options = [arg for arg in sys.argv[1:] if arg.startswith('-')]
call_params = [arg for arg in sys.argv[1:] if not arg.startswith('-')]

if len(call_params) < 2:
    err_out('two parameters required.');

jnpath = call_params[0]
print('jnpath: ' + jnpath)
jnpath = pathstring2list(jnpath)
print(jnpath)

print

jnpattern = call_params[1]
print('jnpattern: ' + jnpattern)
jnpattern = pathstring2list(jnpattern)
print(jnpattern)

print

print('do they match?')
print(is_pathmatch(jnpath, jnpattern))

print


