# trakk: simple cli tasklist with recurrence, checklists, and stats
# Copyright (C) 2014 - 2016  David Ulrich
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import psycopg2
import psycopg2.extras
import yaml
import sys
import types

# http://code.activestate.com/recipes/134892-getch-like-unbuffered-character-reading-from-stdin/
import sys, tty, termios
def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

def trakk_input(msg=""):
	out = ""
	
	sys.stdout.write(msg)
	
	while True:
		ch = getch()
		
		if ord(ch) == 27 or ord(ch) == 13:
			break
		else:
			out = out + ch
			sys.stdout.write(ch)
	
	sys.stdout.write("\n")
	return out

state = {
	"connected": False
}
def shutdown(code=0):
	if state["connected"]:
		if cur: cur.close()
		conn.close()
	sys.exit(code)

conn = None
cur = None

try:
	config = yaml.load(file("config.yaml","r"))
except Exception, e:
	print "config.yaml error:", e
	shutdown(1)


try:
	conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s port=%s" % (
		config["dbname"],
		config["user"],
		config["password"],
		config["host"],
		config["port"]))
	state["connected"] = True
except Exception, e:
	print "Connection error:", e
	shutdown(2)

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


def task_done():
	task_view()
	tid = trakk_input("complete task #: ")
	if tid == "": return
	tid = int(tid)
	if not tid > 0: return
	cur.execute("UPDATE tasks SET TaskStatus = 'Closed' WHERE TaskID = %s",(tid,))
	conn.commit()


def task_new():
	task = trakk_input("task: ")
	if task == "": return
	cur.execute("INSERT INTO tasks (TaskTitle) VALUES (%s)",(task,))
	conn.commit()


def task_view():
	cur.execute("SELECT * FROM tasks WHERE TaskStatus = 'Open'")
	for row in cur:
		print "{0}: {1} {2}".format(row["taskid"],row["tasktitle"],row["taskdescription"])
	

mappings = {
	"f": task_done,
	"F": task_done,
	"n": task_new,
	"N": task_new,
	"p": task_view,
	"P": task_view,
	"x": "exit",
	"X": "exit"
}

while True:
	action = trakk_input("what now? [f=finish,p=print,n=new,x=exit] ")
	
	action = action.strip()
	
	if action == "" or not action in mappings:
		continue
	elif mappings[action] == "exit":
		break
	elif isinstance(mappings[action], types.FunctionType):
		mappings[action]()

shutdown()
