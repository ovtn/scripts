#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import sys
import codecs
import argparse
import time
import glob
import re
import subprocess

# User must set the following parameter
nkf_cmd = 'C:\\Programs\\nkfwin\\nkf.exe'
extensions = ['c','cpp','h']
b_convert_to_utf8 = True


def any2utf8(inencoding, infile, outfile=None):
    #print inencoding
    samename = False

    if not outfile:
        outfile = infile + ".tmp"
        samename = True

    print "Input File : " + infile
    print "Output File: " + outfile


    fin  = codecs.open(infile, 'r', inencoding)
    fout = codecs.open(outfile, 'w', 'utf-8')

    for line in fin:
        fout.write(line)

    fin.close()
    fout.close()

    if samename:
        time.sleep(0.1)
        shutil.move(outfile,infile)



parser = argparse.ArgumentParser(description='any to utf-8')
parser.add_argument('inputdir')

commands = parser.parse_args()
print commands
indir = commands.inputdir


print extensions
for base, dirs, files in os.walk(indir):
    for extension in extensions:
        for file in files:
            str = '.*' + '\.' + extension + '$'
            p = re.compile(str)
            #print base + file
            file2 = p.match(os.path.join(base + file))
            if file2:
                encoding = subprocess.check_output(nkf_cmd + ' -g ' + base + '\\' + file )
                if b_convert_to_utf8 == True:
                    # 改行を含むので文字列範囲を指定する
                    if encoding[0:-1] == 'ASCII':
                     #print file2.group() + ' ' + encoding[0:-1]
                     any2utf8('ascii', base + '\\' + file)
                    elif encoding[0:-1] == 'UTF-8':
                     #print file2.group() + ' ' + encoding[0:-1]
                     any2utf8('utf-8', base + '\\' + file)
                    elif encoding[0:-1] == 'EUC-JP':
                     #print file2.group() + ' ' + encoding[0:-1]
                     any2utf8('euc_jp', base + '\\' + file)
                    elif encoding[0:-1] == 'CP932':
                     #print file2.group() + ' ' + encoding[0:-1]
                     any2utf8('cp932', base + '\\' + file)
                    else:
                     sys.stderr.write( file2.group() + ' Unknown encoding:' + encoding[0:-1] + '\n' )
                else:
                    print file2.group() + ' ' + encoding[0:-1]


sys.exit()


