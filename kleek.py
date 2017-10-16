#!/usr/bin/python
import sys
import subprocess
import time
import argparse
import re

parser = argparse.ArgumentParser(description='Setup some klick, fast !')

parser.add_argument('--tempo', metavar='TEMPO', type=int, nargs='?', help='tempo', default=120)
parser.add_argument('--pattern', metavar='PATTERN', type=str, nargs='?', help='klick pattern string: "X" = strong beat, "x" = minor beat, "." = muted beat', default=sys.stdin)
parser.add_argument('--subdivision', metavar='SUBDIVISION', nargs='?', help='main subdivision (4 = quarter-note, 8 = eigth-note, etc)', default=4)
parser.add_argument('--nosub', action='store_true', help='mute all minor beats (turn \'x\' to \'.\')')
parser.add_argument('--allsub', action='store_true', help='play all minor beats (turn \'.\' to \'x\')')
parser.add_argument('--debug', action='store_true', help='print compiled tempo map')

args = vars(parser.parse_args())


if type(args['pattern']) == file and not sys.stdin.isatty():
    pattern = "".join(args['pattern'].readlines())
else:
    pattern = args['pattern']

pattern = re.sub('[^xX\.]','',pattern, re.MULTILINE)
tempo = str(args['tempo'])
signature = str(len(pattern)) + "/" + str(args['subdivision'])

if args['nosub']:
    pattern = pattern.replace("x",".")

if args['allsub']:
    pattern = pattern.replace(".","x")

if args['debug']:
    print 'Tempo map: ' + ' '.join([signature, tempo, pattern])


try:
    proc = subprocess.Popen(["klick","-P", "9999999", signature, tempo, pattern], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
except:
    print('Failed to start klick')
    raise

print('Klick is playing, hit ctrl+c to stop.')

while True:
    try:
        time.sleep(0.1)
    except:
        break

proc.terminate()
