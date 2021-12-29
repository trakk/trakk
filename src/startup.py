# basic debug environment

import json
import re
import requests
import os
import time

try:
	from pprint import pprint as pp
except e:
	pass


from lib.Config import Config
from lib.Db import Db
from Task import Task


config = Config()
db = Db(config.db)

category_t = "category"
task_t = "task"

category = None
categories = []
tasks = []

def latest_tasks():
	global tasks
	
	ps = []
	where_category = ""
	if category is not None:
		ps.append(category.id)
		where_category = "AND t.category_id = %s"
	q = """
		SELECT
			*
		FROM tasks t
		WHERE 1=1
			AND t.task_status = 'open'
			{}
	""".format(where_category)
	tasks = db.find(q, ps)
	return tasks


def new(item_type="task", **kwargs):
	global categories
	global tasks
	
	if item_type == category_t:
		c = Category(dict(**kwargs))
		c.insert(db)
		categories.append(c)
	elif item_type == task_t:
		t = Task(dict(**kwargs))
		t.insert(db)
		if category is None or t.category_id == category.id:
			tasks.append(t)


def close(item, item_type="task"):
	if item_type == task_t:
		item.task_status = 'closed'
		item.update(db)


# preload some data
latest_tasks()

