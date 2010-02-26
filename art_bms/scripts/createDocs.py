#!/usr/bin/python
"""Creates the HTML documentation"""
import os
import datetime
import sys

from common_script import *

APP_NAME = 'Art BMS'
SETTINGS = 'art_bms.settings'

def main():
	command = 'export PYTHONPATH=..; export DJANGO_SETTINGS_MODULE=%s; epydoc --html . -v -o ../docs/ --name "%s API Docs"' % (SETTINGS, APP_NAME)
	if not call_system(command):
		print 'aborting'
		return

if __name__ == '__main__':
	main()