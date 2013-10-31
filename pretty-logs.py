#!/usr/bin/env python
"""
Pretiffy the logs

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

while (1):
    line = fd.readline()
    if not line: break
    start = find_start(line, 0)
    print line[:start]
    end = find_end(line, start)
    try:
        print json.dumps(json.loads(line[start:end]), indent=4)
    except ValueError:
        if line[start:end].strip(): print line[start:end]
    start = find_start(line, end)
    end = find_end(line, start)
    try:
        print json.dumps(json.loads(line[start:end]), indent=4)
    except ValueError:
        if line[start:end].strip(): print line[start:end]
    print
    print
        

