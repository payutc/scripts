#!/usr/bin/env python
"""
Prettify the logs

Usage:
streaming: tail -f mylogs.log | ./pretty-logs.py 
view: ./pretty-logs.py < mylogs.log

"""
import sys
import json

def find_end(line, start):
    x = 0
    for i,c in enumerate(line[start:]):
        if c in ('{','['):
            x += 1
        elif c in ('}',']'):
            x -= 1
        if x == 0:
            return start+i+1
    return len(line)

def find_start(line, start):
    for i,c in enumerate(line[start:]):
        if c == '{':
            return start+i
    return len(line)

fd = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin

from pprint import pprint
import traceback

def clean(d):
    if isinstance(d, dict):
        for k,v in d.items():
            if k == 'trace':
                trace = []
                for i,l in enumerate(d[k]):
                    s = '{%s} ' % i
                    if 'file' in l:
                        s += l['file']
                        if 'line' in l:
                            s += '(%s)' % l['line']
                        s += ': '
                    if 'class' in l:
                        s += l['class']+l['type']
                    s += '%s(%s)' % (
                        l['function'],
                        ', '.join(( str(x) for x in l['args'] ))
                    )
                    trace.append(s)
                d['trace'] = trace
    return d

while (1):
    line = fd.readline()
    if not line: break
    start = find_start(line, 0)
    print line[:start]
    end = find_end(line, start)
    try:
        d = json.loads(line[start:end])
        d = clean(d)
        print json.dumps(d, indent=4)
    except ValueError:
        traceback.print_exc()
        if line[start:end].strip(): print line[start:end]
    start = find_start(line, end)
    end = find_end(line, start)
    try:
        d = json.loads(line[start:end])
        d = clean(d)
        print json.dumps(d, indent=4)
    except ValueError:
        traceback.print_exc()
        if line[start:end].strip(): print line[start:end]
    print
    print
        

