#! /usr/bin/env python3
#pylint: disable=redefined-variable-type

import sys
from difflib import ndiff
from io import StringIO
from pprint import pformat

from base import mkTree, dictToTrie
from words import Brivla, Cmavo

success = True

class cmavo1(Cmavo):
    pass
class cmavo2(Cmavo):
    pass
class cmavo3(Cmavo):
    pass
class cmavo4(Cmavo):
    pass

def CHECK(name, func, expected):
    '''Pretty prints an output for the comparison between `expected` and the
    value returned by `func()`.'''
    print('Testing for ', name, '... ', sep='', end='')
    got = func()
    if got == expected:
        print("\033[92mOK\033[0m")
        return True
    else:
        print("\033[91mFAIL\033[0m")
        args = {'sep': "\n\t", 'end': "\n\n", 'file': sys.stderr}
        expected_l = expected.splitlines()
        got_l = got.splitlines()
        print('Expected:', *expected_l, **args)
        print('Got:', *got_l, **args)
        diff = list(ndiff(expected_l, got_l))
        print('Diff:', *diff, sep="\n", file=sys.stderr)
        return False

def XCHECK(name, func, expected_type, expected_args):
    '''Runs like CHECK, but expects an exception.'''
    print('Testing for ', name, '... ', sep='', end='')
    try:
        got = func()
    except expected_type as e:
        if e.args == expected_args:
            print("\033[92mFAIL\033[0m")
            return True
        else:
            print("\033[91mFAIL\033[0m")
            args = {'sep': "\n\t", 'end': "\n\n", 'file': sys.stderr}
            print('Expected:', *expected_args, **args)
            print('Got:', *e.args, **args)
            diff = list(ndiff(expected_args, e.args))
            print('Diff:', *diff, sep="\n", file=sys.stderr)
            return False
    except Exception as e: #pylint: disable=broad-except
        print("\033[91mFAIL\033[0m")
        print('Expected ', expected_type.__name__, ', got ', type(e).__name__,
              ': ', e, sep='', file=sys.stderr)
        return False
    else:
        print("\033[91mOK\033[0m")
        print('Expected ', expected_type.__name__, ': ', expected_args, sep='',
              file=sys.stderr)
        print('Got no exception and return value:', got, sep="\n", file=sys.stderr)
        return False

def tester(title, func, in_, expected):
    out = StringIO()
    def caller():
        func(in_, out)
        return out.getvalue()
    passed = CHECK(title, caller, expected)
    out.close()
    return passed

############
## mkTree ##
############

test_mktree = lambda name, node, exp: tester(name, mkTree, node, exp)

test = cmavo1(cmavo2(), cmavo3())
exp = """digraph {
\t0 [label = cmavo1]
\t0 -> 1
\t1 [label = cmavo2]
\t0 -> 2
\t2 [label = cmavo3]
}
"""

success &= test_mktree('mkTree', test, exp)

##################
## descriptions ##
##################

class brivla(Brivla):
    _functions = ['test1', 'test2']

test2 = brivla(cmavo1(), cmavo2())
exp = """digraph {
\t0 [label = brivla]
\t0 -> 1 [label = x1]
\t1 [label = cmavo1]
\t0 -> 2 [color = white]
\t2 [color = white, label = ""]
\t0 -> 3 [label = "test1"]
\t3 [label = cmavo2]
}
"""

success &= test_mktree('descriptions (non exhaustive)', test2, exp)

test2 = brivla(cmavo1(), cmavo2(), cmavo3())
exp = """digraph {
\t0 [label = brivla]
\t0 -> 1 [label = x1]
\t1 [label = cmavo1]
\t0 -> 2 [color = white]
\t2 [color = white, label = ""]
\t0 -> 3 [label = "test1"]
\t3 [label = cmavo2]
\t0 -> 4 [label = "test2"]
\t4 [label = cmavo3]
}
"""

success &= test_mktree('descriptions (exhaustive)', test2, exp)

test2 = brivla(cmavo1(), cmavo2(), cmavo3(), cmavo4())

success &= test_mktree('descriptions (surexhaustive)', test2, exp)

################
## dictToTrie ##
################

test = {'aa': cmavo1, 'ab': cmavo2, 'b': cmavo3}
exp = '''{'a': {'a': <class '__main__.cmavo1'>,
       'b': <class '__main__.cmavo2'>},
 'b': <class '__main__.cmavo3'>}'''

success &= CHECK('dictToTrie',
                 lambda: pformat(dictToTrie(test), width=1),
                 exp)

test = {'a': cmavo1, 'ab': cmavo2}

success &= XCHECK('dictToTrie (with collision)',
                  lambda: pformat(dictToTrie(test), width=1),
                  TypeError,
                  ("'type' object does not support item assignment",))

if success:
    print("Tests passed.\n")
else:
    print("Tests failed.\n")
    sys.exit(1)
