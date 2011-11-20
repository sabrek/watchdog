# -*- coding: utf-8 -*-

# Author: Jacek 'Sabr' Karolak (j.karolak@sabr.pl)
# Watch [files] for change, and after every change run given [command]
#
#
# Example watchdog script: safari.py
#  #!/usr/bin/env python
#  # -*- coding: utf-8 -*-
#
#  from watchdog import Watchdog
#
#  if __name__ == "__main__":
#      Watchdog(["osascript", "-e", """tell application "Safari"
#              do JavaScript "window.location.reload()" in front document
#          end tell"""]).run()
#   EOF
#
# Make safari.py executable (chmox +x safari.py) or use it with python.
# python safari.py FILES_TO_WATCH
# Whenever FILES_TO_WATCH change, refresh Safari in background :-)
#

__all__ = ["Watchdog"]

import argparse, subprocess
from os import getcwd, listdir, stat
from os.path import exists
from time import sleep


class Watchdog(object):

    def __init__(self, cmd):
        self._command = cmd
        self._files_to_watch = set()
        self._file_modification_times = {}

    def _watchdog(self):
        '''Check wheter any file in self._files_to_watch changed,
        if so fire self._command'''

        while True:

            new_modification_times = dict((fn, stat(fn).st_mtime)\
                    for fn in self._files_to_watch)

            if new_modification_times != self._file_modification_times:
                self._file_modification_times = new_modification_times
                subprocess.call(self._command)
                print('Modificaton in files noticed...')

            # sleep before next check
            sleep(0.5)

    def _set_files_to_watch(self, files):
        '''Process args files wheter they exists and include current directory
        content if requested.'''
        if '.' in files:
            files.remove('.')
            # combine all other given files with current working directory
            # content, without dot files
            files += [f for f in listdir(getcwd()) if not f.startswith('.')]

        # make f list unique
        self._files_to_watch = set(files)

        # set modification times
        for fn in self._files_to_watch:
            self._file_modification_times[fn] = stat(fn).st_mtime


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

        self._set_files_to_watch(args.files)

        print('Started watching...')
        self._watchdog()

