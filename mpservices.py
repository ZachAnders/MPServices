#!/usr/bin/python

import os, sys, subprocess

#Launch Daemons directory for OS X
DAEMONS_DIR = "/Library/LaunchDaemons/"

COL_RED = "\033[91m"
COL_GRN = "\033[92m"
COL_END = "\033[0m"

def get_running_daemons():
	lctl = subprocess.Popen(["/bin/launchctl", "list"], stdout=subprocess.PIPE)
	daemons = lctl.stdout.readlines()
	daemons = [line.split("\t") for line in daemons]
	daemons = [line[2].strip() for line in daemons[1:]]
	return daemons
	

def main(outpipe):
	ls = os.listdir(DAEMONS_DIR)

	macports_daemons = [daemon.replace(".plist", "") for daemon in ls if daemon.find("org.macports") == 0]
	running_daemons = [mpdaemon for mpdaemon in get_running_daemons() if "org.macports" in mpdaemon]
	for daemon in macports_daemons:
		daemon = daemon + " "*(60-len(daemon))
		outpipe.write(daemon)
		if daemon in running_daemons:
			col = COL_GRN
			status = "RUNNING"
		else:
			col = COL_RED
			status = "NOT RUNNING"
		outpipe.write("".join([col, status, COL_END, "\n"]))

if __name__ == "__main__":
	main(sys.stdout)
