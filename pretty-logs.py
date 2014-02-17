#!/usr/bin/env python
"""
Prettify the logs

Usage:
streaming: tail -f mylogs.log | ./pretty-logs.py 
view: ./pretty-logs.py < mylogs.log

"""
import sys
import json


fd = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin

from pprint import pprint
import traceback

def format_traceback_part(i, tb_part):
    s = '{%s} ' % i
    if 'file' in tb_part:
        s += tb_part['file']
        if 'line' in tb_part:
            s += '(%s)' % tb_part['line']
        s += ': '
    if 'class' in tb_part:
        s += tb_part['class']+tb_part['type']
    s += '%s(%s)' % (
        tb_part['function'],
        ', '.join(( str(x) for x in tb_part['args'] ))
    )
    return s

def clean(d):
    if isinstance(d, dict):
        for k,v in d.items():
            if k == 'trace' and len(d[k]) > 0 and isinstance(d[k][0], dict):
                trace = []
                for i,l in enumerate(d[k]):
                    s = format_traceback_part(i, l)
                    trace.append(s)
                d['trace'] = trace
            else:
                d[k] = clean(v)
    return d

while (1):
    line = fd.readline()
    if not line: continue
    try:
        d = json.loads(line)
        d = clean(d)
        print json.dumps(d, indent=4)
        #pprint(d)
    except ValueError:
        traceback.print_exc()
        print line
    print
    
        

