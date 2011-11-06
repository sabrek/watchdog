# -*- coding: utf-8 -*-

# Author: Jacek 'Sabr' Karolak (j.karolak@sabr.pl)
# Watch [files] for change, and after every change run given [command]

import argparse, subprocess
from os import getcwd, listdir, stat
from os.path import exists

class Loop(object):

    def __init__(self, cmd):
        self._command = cmd
        self._files_to_watch = {}

    def _set_files_to_watch(self, files):
        '''Process args files wheter they exists and include current directory
        content if requested.'''
        if '.' in files:
            files.remove('.')
            # combine alle other files with current working directory content
            # without dot files
            files += [f for f in listdir(getcwd())\
                    if not f.startswith('.')]

        # make f list unique
        files = set(files)

        # check rights (in order to perform system stat) and wheter they exist
        for f in files:
            if not exists(f):
                msg = 'file \'{}\' does not exists, or I don\'t have access rights.'\
                        .format(f)
                raise IOError(msg)

        # save files to watch in instance variable
        self._files_to_watch = dict.fromkeys(files)

        # set modification times
        for file_key in self._files_to_watch.keys():
            self._files_to_watch[file_key] = stat(file_key).st_mtime


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


