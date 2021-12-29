
import atexit
import os

try:
	import readline
except ImportError:
	print(".pythonrc :: Module readline not available.")
else:
	import rlcompleter

	readline.parse_and_bind("tab: complete")
	print(".pythonrc :: AutoCompletion Loaded")

	# history_file = os.path.join(os.path.expanduser("~"), ".pyhistory")
	history_file = os.path.abspath(os.path.join(os.getcwd(), "../.pyhistory"))
	print(".pythonrc :: history file:", history_file)


	def save_history(history=history_file):
		import readline
		readline.write_history_file(history)
		print(".pythonrc :: history saved to " + history)


	def load_history(history=history_file):
		try:
			readline.read_history_file(history)
		except IOError:
			pass

	load_history()
	atexit.register(save_history)

	del readline, rlcompleter, atexit, history_file

# basic debug environment

import json
import os
from pprint import pprint as pp
import re
import requests
import sys
import time

from Category import Category
from lib.Config import Config
from lib.Db import Db
from Task import Task

sys.displayhook = lambda x: exec(['_=x; pp(x)','pass'][x is None])

config = Config()
db = Db(config.db)

category = None
categories = []
tasks = []

def latest_tasks():
	global category
	global tasks
	
	opt = {}
	if category is not None:
		opt["category"] = category
	tasks = Task.fetch_by_opt(db, **opt)
	return tasks


def new(item_type="Task", **kwargs):
	global categories
	global tasks
	
	if item_type == Category.__name__:
		print("Creating category")
		c = Category(dict(**kwargs))
		c.insert(db)
		categories.append(c)
	elif item_type == Task.__name__:
		print("Creating task")
		opt = dict(**kwargs)
		if category is not None and "category_id" not in opt:
			opt["category_id"] = category.category_id
		t = Task(opt)
		t.insert(db)
		if category is None or t.category_id == category.category_id:
			tasks.append(t)


def new_cat(slug, title):
	return new(item_type="Category", category_slug=slug, category_title=title)
def new_category(slug, title):
	return new(item_type="Category", category_slug=slug, category_title=title)


def new_task(title):
	return new(task_title=title)


def close(item, item_type=""):
	global tasks
	
	if item_type == "":
		item_type = type(item).__name__
	
	if item_type == Task.__name__:
		item.task_status = 'closed'
		item.update(db)
		tasks = list(filter(lambda t: t.task_id != item.task_id, tasks))
		return tasks


def use(item):
	global category
	global tasks
	
	item_type = type(item).__name__
	if item_type == Category.__name__:
		category = item
		tasks = Task.fetch_by_opt(db, category=category)
		pp(category)
		return tasks
	elif item_type == 'str':
		cs = list(filter(lambda c: c.category_slug == item, categories))
		if len(cs) == 1:
			category = cs[0]
			tasks = Task.fetch_by_opt(db, category=category)
			pp(category)
			return tasks
		else:
			print(f"unknown category: {item}")


# preload some data
categories = Category.fetch_by_opt(db)
latest_tasks()




