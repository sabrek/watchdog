# -*- coding: utf-8 -*-

# Author: Jacek 'Sabr' Karolak (j.karolak@sabr.pl)
# Watch [files] for change, and after every change run given [command]

import argparse, subprocess


class Loop(object):

    def __init__(self, cmd):
        self._command = cmd
        self._files_to_watch = {}
