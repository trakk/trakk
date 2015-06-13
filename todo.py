# todo: simple cli tasklist with recurrence, checklists, and stats
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

import json
import psycopg2
import yaml



def shutdown():
	if

try:
	config = yaml.load(file("config.yaml","r"))
except yaml.YAMLError, e:
	print "config.yaml error:", e
	shutdown()


try:
	conn = psycopg2.connect("dbname=todo user=todo password=34dS&9ttttt port=5433")
	
except psycopg2.Error, e:
	print "Connection error:", e
	shutdown()

print config

cur = conn.cursor()

#cur.execute("CREATE TABLE IF NOT EXISTS items (ItemID SERIAL PRIMARY KEY,Description VARCHAR)")
#cur.execute("INSERT INTO items (Description) VALUES (%s)",("learn python",))
conn.commit()

cur.execute("SELECT * FROM items")

print cur.fetchone()

cur.close()
conn.close()
