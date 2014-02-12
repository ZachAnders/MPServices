#!/usr/bin/python

import os, subprocess

#Launch Daemons directory for OS X
DAEMONS_DIR = "/Library/LaunchDaemons/"

def get_running_daemons(macports_only=True):
	lctl = subprocess.Popen(["/bin/launchctl", "list"], stdout=subprocess.PIPE)
	daemons = lctl.stdout.readlines()
	daemons = [line.split("\t") for line in daemons]
	daemons = [line[2].strip() for line in daemons[1:]]
	if macports_only:
		daemons = [mpdaemon for mpdaemon in daemons if "org.macports" in mpdaemon]
	return daemons

def get_all_daemons(macports_only=True):
	ls = os.listdir(DAEMONS_DIR)
	daemons = [daemon.replace(".plist", "") for daemon in ls]
	if macports_only:
		daemons = [daemon for daemon in daemons if "org.macports." in daemon] 
	return daemons

def do(service, action):
	if action == "load":
		return load(service)
	elif action == "reload":
		return unload(service) | load(service)
	elif action == "unload":
		return unload(service)

def __call(service, cmd, sudo=True):
	return subprocess.call(["sudo"*sudo, "launchctl", cmd, "-w", DAEMONS_DIR+service+".plist"])

def load(service):
	return __call(service, "load")
	

def unload(service):
	return __call(service, "unload")


