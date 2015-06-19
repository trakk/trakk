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
import yaml
import sys


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
	conn = psycopg2.connect("dbname=%s user=%s password=%s port=%s" % (
		config["dbname"],
		config["user"],
		config["password"],
		config["port"]))
	state["connected"] = True
except psycopg2.Error, e:
	print "Connection error:", e
	shutdown(2)

print config

cur = conn.cursor()


while True:
	action = raw_input("what now? [p=print,n=new,x=exit] ")
	
	if action == "n":
		task = raw_input("task: ")
		cur.execute("INSERT INTO tasks (TaskTitle) VALUES (%s)",(task,))
		conn.commit()
	elif action == "p":
		cur.execute("SELECT * FROM tasks")
		print cur.fetchall()
	elif action == "x":
		break

shutdown()
