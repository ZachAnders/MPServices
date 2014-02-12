#!/usr/bin/python
import sys
import osxdaemons

COL_RED = "\033[91m"
COL_GRN = "\033[92m"
COL_END = "\033[0m"

load_actions = ["up", "on", "load", "start"] 
unload_actions = ["down", "off", "unload", "stop"]

ACTIONS = {act:"load"  for act in load_actions}
ACTIONS.update({act:"unload" for act in unload_actions})

def usage():
	sname = str(sys.argv[0])
	print("Lists or starts/stops macports related services.")
	print("Usage: ./" + sname + " [<service name> <verb>] ")
	print("Valid verbs: ")
	

def match_service(sname):
	matches = [daemon for daemon in osxdaemons.get_all_daemons() if sname in daemon]
	if len(matches) > 1:
		print("Matched too many services:\n")
		for match in matches:
			print("> " + match + "\n")
		return None
	#print("Found service: " + matches[0] + "\n")
	return matches[0]

def match_action(action):
	if action in ACTIONS:
		action = ACTIONS[action]
		return action
	else:
		return None


def service_action(service, action):
	action = match_action(action)
	if action:
		print(action.title() + "ing service: " + service)
		return osxdaemons.do(service, action)
	else:
		print("Wtf I don't know how to " + action + ".")
		usage()
		return -1

	
def print_services():
	running_daemons = osxdaemons.get_running_daemons()
	for daemon in osxdaemons.get_all_daemons():
		outs = daemon + " "*(60-len(daemon))
		if daemon in running_daemons:
			col = COL_GRN
			status = "RUNNING"
		else:
			col = COL_RED
			status = "NOT RUNNING"
		print(outs + col + status + COL_END)

def main():
	if len(sys.argv) == 1:
		print_services()
		return 0
	elif len(sys.argv) == 3:
		sname, action = sys.argv[1:3]
		sname = match_service(sname)
		return service_action(sname, action)
	else:
		usage()
		return 0

if __name__ == "__main__":
	sys.exit(main())
