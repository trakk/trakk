# trakk: simple cli tasklist with recurrence, checklists, and stats
# Copyright (C) 2014 - 2015  David Ulrich
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


state = {
	"connected": True
}
def shutdown(code=0):
	if state["connected"]:
		cur.close()
		conn.close()
	sys.exit(code)

try:
	config = yaml.load(file("config.yaml","r"))
except yaml.YAMLError, e:
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
except psycopg2.Error, e:
	print "Connection error:", e
	shutdown(2)

print config

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


def task_done():
	task_view()
	tid = raw_input("complete task #: ")
	cur.execute("UPDATE tasks SET TaskComplete = TRUE WHERE TaskID = %s",(tid,))
	conn.commit()


def task_new():
	task = raw_input("task: ")
	cur.execute("INSERT INTO tasks (TaskTitle) VALUES (%s)",(task,))
	conn.commit()


def task_view():
	cur.execute("SELECT * FROM tasks WHERE NOT TaskComplete")
	for row in cur:
		print "{0}: {1} {2}".format(row["taskid"],row["tasktitle"],row["taskdescription"])
	

mappings = {
	"d": task_done,
	"D": task_done,
	"n": task_new,
	"N": task_new,
	"p": task_view,
	"P": task_view,
	"x": "exit",
	"X": "exit"
}

while True:
	action = raw_input("what now? [d=done,p=print,n=new,x=exit] ")
	
	if action == "" or not action in mappings:
		continue
	elif mappings[action] == "exit":
		break
	elif isinstance(mappings[action], types.FunctionType):
		mappings[action]()

shutdown()
