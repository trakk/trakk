
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
all_categories = {}
all_tasks = {}


def load_tasks():
	global all_tasks
	global category
	
	category = Category(dict(category_id=None, category_slug="none"))
	all_tasks = { None: [] }
	opt = {}
	ts = Task.fetch_by_opt(db, **opt)
	for t in ts:
		if not t.category_id in all_tasks:
			all_tasks[t.category_id] = []
		all_tasks[t.category_id].append(t)


def new(item_type="Task", **kwargs):
	global all_tasks
	global categories
	
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
		all_tasks[t.category_id].append(t)


def new_cat(slug, title):
	return new(item_type="Category", category_slug=slug, category_title=title)
def new_category(slug, title):
	return new(item_type="Category", category_slug=slug, category_title=title)


def new_task(title):
	return new(task_title=title)


def close(item, item_type=""):
	if item_type == "":
		item_type = type(item).__name__
	
	if item_type == Task.__name__:
		close_task(item)
		tasks()
	elif item_type == 'int':
		task = all_tasks[category.category_id][item-1]
		close_task(task)
		tasks()


def close_task(task):
	global all_tasks
	
	task.task_status = 'closed'
	task.update(db)
	all_tasks[task.category_id] = list(filter(lambda t: t.task_id != task.task_id, all_tasks[task.category_id]))


def cats():
    global all_tasks
    global categories
    global all_categories

    all_categories[None] = Category(dict(category_id=None, category_slug="none"))
    for c in categories:
        all_categories[c.category_id] = c
    for cid in all_tasks.keys():
        all_categories[cid].tasks = all_tasks[cid]
    for cid in all_categories.keys():
        c = all_categories[cid]
        print(f"{c.category_slug.ljust(12, ' ')} [{len(c.tasks)}]: {c.category_title}")


def tasks():
	global all_tasks
	global category
	
	if not category.category_id in all_tasks:
		all_tasks[category.category_id] = []
	
	for i, task in enumerate(all_tasks[category.category_id]):
		 print(f"{i+1}: {task.task_title} [{task.task_id}]")


def use(item):
	global category
	
	item_type = type(item).__name__
	if item_type == Category.__name__:
		category = item
		sys.ps1 = category.category_slug + ">"
		pp(category)
		tasks()
	elif item_type == 'str':
		cs = list(filter(lambda c: c.category_slug == item, categories))
		if len(cs) == 1:
			category = cs[0]
			sys.ps1 = category.category_slug + ">"
			pp(category)
			tasks()
		else:
			print(f"unknown category: {item}")


# preload some data
categories = Category.fetch_by_opt(db)
load_tasks()




