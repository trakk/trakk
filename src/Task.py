class Task():
	_defs = [
		("task_id", ""),
		("category_id", None),
		("task_title", ""),
		("task_description", ""),
		("task_status", "open")
	]
	_attr = [d[0] for d in _defs]

	def __init__(self, data=None):
		if data is None:
			data = {}
		self.merge(data)


	def __repr__(self):
		return f"{self.task_title} [{self.task_id}]"


	def __str__(self):
		return f"{self.task_title}"


	def merge(self, data=None):
		if data is None:
			data = {}
		for field, default, *_type in type(self)._defs:
			if _type:
				value = _type[0](data[field]) if field in data else default
			else:
				value = data[field] if field in data else default
			setattr(self, field, value)


	def asdict(self):
		d = {}
		for field in type(self)._attr:
			value = getattr(self, field)
			if hasattr(value, "asdict") and callable(value.asdict):
				value = value.asdict()
			d[field] = value
		return d


	def delete(self, db):
		q = """
			DELETE FROM tasks WHERE task_id = %s
		"""
		ps = (self.task_id,)
		db.do(q, ps)


	def fetch(self, db):
		q = """
			SELECT
				*
			FROM tasks t
			WHERE 1=1
				AND t.task_id = %s
		"""
		ps = (self.task_id,)
		row = db.find_one(q, ps)
		self.merge(row)


	@classmethod
	def fetch_by_id(class_obj, task_id, db):
		t = class_obj(dict(task_id=task_id))
		t.fetch(db)
		return t
	
	
	@classmethod
	def fetch_by_opt(class_obj, db, **kwargs):
		opt = {**kwargs}
		
		ps = []
		where_category = ""
		if "category" in opt and opt["category"] is not None:
			ps.append(opt["category"].category_id)
			where_category = "AND t.category_id = %s"
		q = """
			SELECT
				*
			FROM tasks t
			WHERE 1=1
				AND t.task_status = 'open'
				{}
		""".format(where_category)
		rows = db.find(q, ps)
		tasks = [class_obj(t) for t in rows]
		return tasks


	def insert(self, db):
		q = """
			INSERT INTO tasks (category_id, task_title, task_description, task_status)
			VALUES
			(%s, %s, %s, %s)
			RETURNING task_id
		"""
		ps = (self.category_id, self.task_title, self.task_description, self.task_status)
		row = db.find_one(q, ps)
		self.task_id = row["task_id"]


	def update(self, db):
		q = """
			INSERT INTO tasks (task_id, category_id, task_title, task_description, task_status)
			VALUES
			(%s, %s, %s, %s, %s)
			ON CONFLICT (task_id)
			DO UPDATE SET
				category_id=EXCLUDED.category_id,
				task_title=EXCLUDED.task_title,
				task_description=EXCLUDED.task_description,
				task_status=EXCLUDED.task_status
		"""
		ps = (self.task_id, self.category_id, self.task_title, self.task_description, self.task_status)
		db.do(q, ps)






