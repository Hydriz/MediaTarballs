#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Hydriz
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import urllib

# Global configuration
# S3-like API keys (Get one at http://archive.org/account/s3.php
accesskey = ""
secretkey = ""
# Dump files
host = ""
incrdate = ""
# Archive.org matters
collection = ""
mediatype = ""
# Other stuff
wikifilelist = "result.txt" # /path/to/result.txt
sizehint = "107374182400" # 100GB

# Nothing to change below...
filelist = {
	'local-media-incr.gz',
	'remote-media-incr.gz',
}
def welcome():
	print "Scans the listing directory for wikis that have incremental dumps generated for them"

def bye():
	print "Done uploading. Bye!"

def listofwikis():
	wikilist = open(wikifilelist).read().splitlines()
	for wiki in wikilist:
		for gzfile in filelist:
			listfile = ''.join(gzfile)
			nicename = wiki + "-" + incrdate + "-" + listfile
			wgetthefile(nicename)
			upload(nicename)

def upload(thedumpfile):
	firstfile = "abwiki" + "-" + incrdate + "-remote-media-incr.gz"
	if (thedumpfile == firstfile):
		curl = ['curl', '--retry 20', '--location',
				'--header', "'x-amz-auto-make-bucket:1'",
				'--header', "'x-archive-meta01-collection:%s'" % (collection),
				'--header', "'x-archive-meta-mediatype:%s'" % (mediatype),
				'--header', "'x-archive-queue-derive:0'",
				'--header', "'x-archive-size-hint:%s'" % (sizehint),
				'--header', "'x-archive-meta-title:Wikimedia media dumps incrementals file list for %s'" % (incrdate),
				'--header', "'x-archive-meta-description:This is the incremental media dumps file list generated by Wikimedia on %s.'" % (incrdate),
				'--header', '"authorization: LOW %s:%s"' % (accesskey,secretkey),
				'--upload-file', "%s http://s3.us.archive.org/mediatar-%s-list/%s" % (thedumpfile,incrdate,thedumpfile),
				]
		os.system(' '.join(curl))
		rmcmd = "rm " + thedumpfile
		os.system(rmcmd)
		os.system("sleep 60")
	else:
		curl = ['curl', '--retry 20', '--location',
				'--header', "'x-archive-queue-derive:0'",
				'--header', '"authorization: LOW %s:%s"' % (accesskey,secretkey),
				'--upload-file', "%s http://s3.us.archive.org/mediatar-%s-list/%s" % (thedumpfile,incrdate,thedumpfile),
				]
		os.system(' '.join(curl))
		rmcmd = "rm " + thedumpfile
		os.system(rmcmd)

def wgetthefile(thedumpfile):
	os.system("wget -c " + host + thedumpfile)

def process():
	welcome()
	listofwikis()
	bye()

process()
