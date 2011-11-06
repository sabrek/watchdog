# -*- coding: utf-8 -*-

# Author: Jacek 'Sabr' Karolak (j.karolak@sabr.pl)
# Watch [files] for change, and after every change run given [command]

import argparse, subprocess


class Loop(object):

    def __init__(self, cmd):
        self._command = cmd
        self._files_to_watch = {}

    def run(self):
        '''Parses command line arguments, processes files list,
        and fires watchdog.'''
        parser = argparse.ArgumentParser(description='Checkes wheter given \
                files change, when they do, runs given command.')
        parser.add_argument('files', metavar='F', type=str, nargs='+',\
                help='list files to process, if you add . in list it will\
                watch also all non dot files in current dir.\
                If you want to have all non dot files and some dot ones use:\
                \n.file1 .file2 .file2 . .file3 it will combine specified dot\
                files and all others.')

        args = parser.parse_args()

